# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, List, Any, Callable, Set, Tuple
import logging
import os

from joblib import Parallel, delayed, parallel_backend
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesDfMultiFrequenciesDiff,
    TimeseriesDsFreqLessThenFcFreq,
    TimeseriesDfFrequencyNotConsistent)
from azureml.automl.core.shared.constants import (
    ShortSeriesHandlingValues,
    TimeSeries,
    TimeSeriesInternal,
    TimeSeriesWebLinks
)
from azureml.automl.core.shared.forecasting_exception import (
    ForecastingConfigException,
    ForecastingDataException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.utilities import get_min_points
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil
from azureml.train.automl.runtime._automl_job_phases.worker_initiator import get_worker_variables
from azureml.train.automl.runtime._partitioned_dataset_utils import (
    _get_dataset_for_grain,
    _to_dask_dataframe_of_random_grains
)
from azureml.automl.runtime._freq_aggregator import _get_frequency_nanos
from azureml.automl.runtime._grain_preparer import _preprocess_grain, _validate_grain_by_dataset, GrainPreprocessResult
from azureml.automl.runtime._grain_stat_generator import _get_grain_stat, GrainStatistics
from azureml.automl.runtime.column_purpose_detection import _time_series_column_helper
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurizer.transformer.timeseries.forecasting_heuristic_utils import (
    frequency_based_lags,
    try_get_auto_parameters
)
from azureml.automl.runtime.frequency_fixer import FREQUENCY_REJECT_TOLERANCE
from azureml.automl.runtime.shared.time_series_data_frame import construct_tsdf

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class DistributedPreparationPhase:
    """AutoML job phase that prepares the data."""

    @staticmethod
    def run(workspace_getter: Callable[..., Any],
            experiment_name: str,
            parent_run_id: str,
            automl_settings: AzureAutoMLSettings,
            training_dataset: TabularDataset,
            validation_dataset: TabularDataset,
            verifier: VerifierManager,
            parallel_backend_name: str = 'dask') -> None:

        """
        We do following this in this function
        We do grain statistics calculation in distributed way
        We do make some centralized decisions and stat summary calculations based on gathered statistics
        We do some centralized validations that cant be done in distributed way
        We then prepare data in distributed way (fixing frequency, aggregating and padding short series)
        We then invoke grain by grain validation in distributed way
        We then do train/valid split
        """

        PhaseUtil.log_with_memory("Beginning distributed preparation")

        # In non-distributed runs frequency calculation on the tsdf happens by
        # taking the mode frequency of the full tsdf. Since we cannot do that with
        # distribution without an additional full pass on data, we subsample to 100
        # grains and then infer_freq on those.
        subsampled_grains_ddf = _to_dask_dataframe_of_random_grains(training_dataset, 100)
        subsampled_X = subsampled_grains_ddf.compute()
        subsampled_Y = subsampled_X.pop(automl_settings.label_column_name).values

        tsdf = construct_tsdf(
            subsampled_X,
            subsampled_Y,
            automl_settings.label_column_name,
            automl_settings.time_column_name,
            TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT,
            automl_settings.grain_column_names or [TimeSeriesInternal.DUMMY_GRAIN_COLUMN],
            None  # type: ignore
        )

        tsdf_freq_offset = tsdf.infer_freq()

        # Compute auto parameters with subset of grains
        # For now we disable lags and rolling windows as FTCN
        # doesnt use these features
        _, _, max_horizon = try_get_auto_parameters(
            automl_settings,
            subsampled_X,
            subsampled_Y
        )

        # If doing train/valid split ensure validation and training data is at least 1 full horizon.
        # We don't currently support CV so we pass none here.
        min_points_per_grain = get_min_points(0, [0], max_horizon, None)
        min_points_per_grain *= 2

        grain_stats = None
        with parallel_backend(parallel_backend_name):
            grain_stats = Parallel(n_jobs=-1)(delayed(_get_grain_stat)(
                _get_dataset_for_grain(grain_key_value, training_dataset),
                grain_key_value,
                tsdf_freq_offset,
                automl_settings,
            ) for grain_key_value in training_dataset.get_partition_key_values())

        # we now have stat for all grains. Validate and consolidate
        (
            new_frequency,
            should_aggregate,
            should_pad,
            global_series_start,
            global_series_end
        ) = validate_and_infer_global(
            automl_settings,
            grain_stats,
            min_points_per_grain
        )

        expr_store = ExperimentStore.get_instance()
        expr_store.metadata.timeseries.global_series_start = global_series_start
        expr_store.metadata.timeseries.global_series_end = global_series_end

        if validation_dataset is None:
            if should_aggregate and (_get_frequency_nanos(automl_settings.freq) < _get_frequency_nanos(new_frequency)):
                forecast_freqstr = \
                    automl_settings.freq if isinstance(automl_settings.freq, str) else automl_settings.freq.freqstr
                raise ForecastingConfigException._with_error(
                    AzureMLError.create(
                        TimeseriesDsFreqLessThenFcFreq, target=TimeSeries.FREQUENCY,
                        reference_code=ReferenceCodes._FORECASTING_PARAM_USER_FREQ_DISTRIBUTED,
                        data_freq=new_frequency.freqstr,
                        forecast_freq=forecast_freqstr,
                        freq_doc=TimeSeriesWebLinks.FORECAST_PARAM_DOCS
                    )
                )

            start_times = [grain_stat.start_time for grain_stat in grain_stats]
            prepared_data_dir = '{}_{}_prepared'.format(experiment_name, parent_run_id)

            # Get aggregate column types. Do this by taking the first 10000 rows and assume
            # it is representative of the dataset.
            data_subset = training_dataset.take(10000).to_pandas_dataframe()

            featurization_config = FeaturizationConfig()
            if isinstance(automl_settings.featurization, dict):
                # If user passed in a featurization config, update default with their configuration.
                featurization_config = featurization_config._from_dict(automl_settings.featurization)

            # These should be cached as StatsAndColumnPurpose
            numeric_columns = _time_series_column_helper.get_numeric_columns(
                data_subset, automl_settings.time_column_name,
                automl_settings.grain_column_names, featurization_config)  # type: Set[Any]
            datetime_columns = _time_series_column_helper.get_datetime_columns(
                data_subset, automl_settings.time_column_name,
                automl_settings.grain_column_names, featurization_config)  # type: Set[Any]

            current_purposes = featurization_config.column_purposes or {}

            for col in numeric_columns:
                if col not in current_purposes and col != automl_settings.label_column_name:
                    current_purposes[col] = FeatureType.Numeric
            for col in datetime_columns:
                if col not in current_purposes:
                    current_purposes[col] = FeatureType.DateTime

            featurization_config.column_purposes = current_purposes
            # TODO: make sure this is saved for featurization phase (and onward)
            # if aggregation is enabled for now we cannot persist this VSO: 1326498
            automl_settings.featurization = featurization_config.__dict__

            with logging_utilities.log_activity(logger=logger, activity_name='DistributedPreparation'):
                with parallel_backend(parallel_backend_name):
                    grain_preprocess_results = Parallel(n_jobs=-1)(delayed(_preprocess_one_grain)(
                        workspace_getter,
                        prepared_data_dir,
                        parent_run_id,
                        _get_dataset_for_grain(grain_key_value, training_dataset),
                        grain_key_value,
                        new_frequency,
                        max_horizon,
                        start_time,
                        min_points_per_grain,
                        automl_settings,
                        should_aggregate,
                        should_pad
                    ) for grain_key_value, start_time in zip(training_dataset.get_partition_key_values(), start_times))

            report_prepare_results(verifier, grain_preprocess_results, automl_settings)

            expr_store = ExperimentStore.get_instance()
            expr_store.data.partitioned.save_prepared_train_dataset(
                workspace_getter(),
                prepared_data_dir + "_train",
                training_dataset.partition_keys
            )
            expr_store.data.partitioned.save_prepared_valid_dataset(
                workspace_getter(),
                prepared_data_dir + "_validation",
                training_dataset.partition_keys
            )
        else:
            with logging_utilities.log_activity(logger=logger, activity_name='DistributedValidation'):
                with parallel_backend(parallel_backend_name):
                    Parallel(n_jobs=-1)(delayed(_validate_grain_by_dataset)(
                        _get_dataset_for_grain(grain_key_value, training_dataset),
                        _get_dataset_for_grain(grain_key_value, validation_dataset),
                        automl_settings
                    ) for grain_key_value in training_dataset.get_partition_key_values())

    PhaseUtil.log_with_memory("Ending distributed preparation")


def _preprocess_one_grain(
    workspace_getter: Callable[..., Any],
    prepared_data_data_dir: str,
    parent_run_id: str,
    training_dataset_for_grain: TabularDataset,
    grain_keys_values: Dict[str, Any],
    new_frequency: pd.DateOffset,
    max_horizon: int,
    start_time: pd.Timestamp,
    min_points_per_grain: int,
    automl_settings: AzureAutoMLSettings,
    should_aggregate: bool,
    should_pad: bool
) -> GrainPreprocessResult:

    default_datastore_for_worker, workspace_for_worker, expr_store_for_worker = get_worker_variables(
        workspace_getter, parent_run_id)
    os.makedirs(prepared_data_data_dir, exist_ok=True)

    # load pandas dataframe for one grain
    train_X_grain = training_dataset_for_grain.to_pandas_dataframe()

    # transform one grain
    train_prepared_data, validation_prepared_data, grain_preprocess_result = _preprocess_grain(
        train_X_grain,
        grain_keys_values,
        new_frequency,
        max_horizon,
        start_time,
        min_points_per_grain,
        automl_settings,
        should_aggregate,
        should_pad
    )
    for prepared_data, split in \
            zip([train_prepared_data, validation_prepared_data], ['train', 'validation']):
        # write one grain to local file
        # drop the grain columns since they will be part of the path and hence
        # they will be reconstructed as part of reading partitioned dataset
        prepared_data.reset_index(inplace=True, drop=True)
        prepared_data.drop(columns=automl_settings.grain_column_names, inplace=True)
        grain_keys_values_str = '-'.join([str(v) for v in grain_keys_values.values()])
        prepared_file_name = '{}-{}.parquet'.format(split, grain_keys_values_str)
        prepared_file_path = '{}/{}'.format(prepared_data_data_dir, prepared_file_name)
        prepared_data.to_parquet(prepared_file_path)

        # construct the path to which data will be written to on the default blob store
        target_path_array = ['_'.join([prepared_data_data_dir, split])]
        for val in grain_keys_values.values():
            target_path_array.append(str(val))
        target_path = '/'.join(target_path_array)

        # upload data to default store
        expr_store_for_worker.data.partitioned.write_file(prepared_file_path, target_path)
        logger.info("prepared one grain and uploaded data")

    return grain_preprocess_result


def validate_and_infer_global(
    automl_settings: AzureAutoMLSettings,
    grain_stats: List[GrainStatistics],
    min_points_per_grain: int
) -> Tuple[pd.DateOffset, bool, bool, pd.Timestamp, pd.Timestamp]:
    """
    This method is runs on driver node and is responsible for few things
    Validate global statistics -- such as all grains have same frequency
    Summarize global statistics
    Make global decisions such as following
        -- whether there is need to prepare data (either it is already good OR cant be fixed)
        -- what is common inferred frequency
    """
    frequencies_not_nan = [grain_stat.frequency for grain_stat in grain_stats if grain_stat.frequency is not None]

    # Longest grain will be the longest set of non-null target values
    longest_grain = max([grain_stat.total_rows - grain_stat.n_null_target for grain_stat in grain_stats])
    unique_frequencies = list(set(frequencies_not_nan))
    if len(unique_frequencies) != 1:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfMultiFrequenciesDiff, target='freq',
                                reference_code=ReferenceCodes._DIST_DATA_PREP_MULTI_FREQUENCIES_DIFF))

    should_aggregate = automl_settings.target_aggregation_function is not None and automl_settings.freq is not None

    global_series_start = min([grain_stat.start_time for grain_stat in grain_stats])
    global_series_end = min([grain_stat.end_time for grain_stat in grain_stats])

    new_frequency = unique_frequencies[0]
    total_rows_in_coverage = sum([grain_stat.total_rows_in_coverage for grain_stat in grain_stats
                                  if grain_stat.frequency is not None])
    total_rows = sum([grain_stat.total_rows for grain_stat in grain_stats])

    if total_rows_in_coverage / total_rows < FREQUENCY_REJECT_TOLERANCE:
        raise ForecastingDataException._with_error(
            AzureMLError.create(
                TimeseriesDfFrequencyNotConsistent,
                target='forecasting_parameters/freq',
                reference_code=ReferenceCodes._DIST_DATA_PREP_INCONSISTENT_FREQUENCY,
                freq=str(new_frequency),
                forecasting_config=TimeSeriesWebLinks.FORECAST_CONFIG_DOC))

    should_aggregate = automl_settings.target_aggregation_function is not None and automl_settings.freq is not None

    # if short series handling is Auto and at least one grain is long enough or
    # short series handling is disabled, dont pad.
    if (
        automl_settings.short_series_handling_configuration == ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO and
        longest_grain > min_points_per_grain
    ):
        should_pad = False
    elif (
        automl_settings.short_series_handling_configuration not in
        {
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO,
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        }
    ):
        should_pad = False
    else:
        should_pad = True

    logger.info(
        "The following settings have been identified:"
        "\n\tnew_frequency: {}\n\tshould_aggregate: {}\n\tshould_pad: {}"
        .format(new_frequency, should_aggregate, should_pad)
    )
    return new_frequency, should_aggregate, should_pad, global_series_start, global_series_end


def report_prepare_results(verifier: VerifierManager,
                           grain_preprocess_results: List[GrainPreprocessResult],
                           automl_settings: AzureAutoMLSettings) -> None:
    grains_padded = [g.name for g in filter(lambda x: x.is_padded, grain_preprocess_results)]
    grains_aggregated = len([g.is_aggregated for g in grain_preprocess_results if g.is_aggregated is True])
    grains_freq_fixed = len([g.is_frequency_fixed for g in grain_preprocess_results if g.is_frequency_fixed is True])

    logger.info(
        "Preprocessing results for all grains:"
        "\n\tgrains_padded: {}\n\tgrains_aggregated: {}\n\tgrains_freq_fixed: {}"
        .format(grains_padded, grains_aggregated, grains_freq_fixed)
    )

    verifier.update_data_verifier_aggregation(grains_aggregated > 0,
                                              automl_settings.target_aggregation_function,
                                              automl_settings.freq)
    verifier.update_data_verifier_frequency_inference(False, grains_freq_fixed > 0)
    verifier.update_data_verifier_short_grain_handling(grains_padded, [])
