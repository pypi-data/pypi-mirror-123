from datetime import datetime
from typing import *

import numpy as np
import pandas
import pendulum
import pyspark
from pyspark.sql import DataFrame
from pyspark.sql.utils import AnalysisException

import tecton
from tecton import conf
from tecton._internals import data_frame_helper
from tecton._internals import errors
from tecton._internals import feature_retrieval_internal
from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.errors import FV_INVALID_MOCK_INPUTS
from tecton._internals.feature_packages import aggregations
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.feature_services.query_helper import _QueryHelper
from tecton.interactive.data_frame import DataFrame as TectonDataFrame
from tecton.interactive.data_frame import FeatureVector
from tecton.interactive.dataset import Dataset
from tecton.interactive.feature_definition import FeatureDefinition
from tecton.interactive.run_api import run_batch
from tecton.interactive.run_api import run_ondemand
from tecton.interactive.run_api import run_stream
from tecton.tecton_context import TectonContext
from tecton_proto.args.virtual_data_source_pb2 import DataSourceType
from tecton_proto.data import feature_view_pb2
from tecton_proto.metadataservice.metadata_service_pb2 import GetFeatureViewRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetServingStatusRequest
from tecton_spark import pipeline_helper
from tecton_spark.feature_package_view import FeaturePackageOrView
from tecton_spark.logger import get_logger
from tecton_spark.materialization_params import MaterializationParams
from tecton_spark.pipeline_helper import find_request_context
from tecton_spark.pipeline_helper import pipeline_to_dataframe
from tecton_spark.pipeline_helper import run_mock_pandas_pipeline
from tecton_spark.transformation import RequestContext

logger = get_logger("FeatureView")


__all__ = ["FeatureView", "get_feature_view"]


class FeatureView(FeatureDefinition):
    """
    FeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    _proto: feature_view_pb2.FeatureView

    def __init__(self, proto):
        self._proto = proto

    @classmethod
    def _fco_type_name_singular_snake_case(cls) -> str:
        return "feature_view"

    @classmethod
    def _fco_type_name_plural_snake_case(cls) -> str:
        return "feature_views"

    def __str__(self):
        return f"FeatureView|{self.id}"

    def __repr__(self):
        return f"FeatureView(name='{self.name}')"

    @property  # type: ignore
    @sdk_public_method
    def features(self) -> List[str]:
        """
        Returns the names of the (output) features.
        """
        if self.is_temporal_aggregate:
            feature_names = [f.output_feature_name for f in self._proto.temporal_aggregate.features]
            return [f for f in feature_names if f != self.timestamp_key]

        return super().features

    @sdk_public_method
    def run(self, **mock_inputs: Union[pandas.DataFrame, DataFrame]):
        """
        Runs the feature view against passed-in mock data rather than the actual data sources.

        :param mock_inputs: kwargs with the same expected keys as the FeatureView's inputs parameter. Each input name maps to a Pandas DataFrame that should be evaluated for that node in the pipeline.
        """
        input_names = pipeline_helper.get_all_input_keys(self._proto.pipeline.root)
        if input_names != mock_inputs.keys():
            raise FV_INVALID_MOCK_INPUTS(mock_inputs.keys(), input_names)

        if self.is_online:
            return run_mock_pandas_pipeline(
                self._proto.pipeline, self._proto.enrichments.transformations, self.name, mock_inputs
            )
        else:
            tc = TectonContext.get_instance()
            spark = tc._spark
            return pipeline_to_dataframe(
                spark,
                pipeline=self._proto.pipeline,
                consume_streaming_data_sources=False,
                virtual_data_sources=[],
                transformations=self._proto.enrichments.transformations,
                feature_time_limits=None,
                schedule_interval=pendulum.Duration(
                    seconds=self._proto.materialization_params.schedule_interval.ToSeconds()
                ),
                mock_inputs=mock_inputs,
            )

    def _get_serving_status(self):
        request = GetServingStatusRequest()
        request.feature_package_id.CopyFrom(self._proto.feature_view_id)
        request.workspace = self.workspace
        return metadata_service.instance().GetServingStatus(request)

    @sdk_public_method
    def preview(self, limit=10, time_range: Optional[pendulum.Period] = None, use_materialized_data: bool = True):
        """
        Shows a preview of the FeatureView's features. Random, unique join_keys are chosen to showcase the features.

        :param limit: (Optional, default=10) The number of rows to preview
        :param time_range: (Optional) Time range to collect features from. Will default to recent data (past 2 days).
        :param use_materialized_data: (Optional) Use materialized data if materialization is enabled.
        :return: A Tecton :class:`DataFrame`.
        """
        if self.is_online:
            raise errors.FP_NOT_SUPPORTED_GET_FEATURE_DF

        try:
            pandas_df = (
                data_frame_helper._get_feature_dataframe_with_limits(
                    FeaturePackageOrView.of(self._proto),
                    spine=None,
                    spine_time_key=None,
                    spine_time_limits=time_range,
                    use_materialized_data=use_materialized_data,
                )
                .to_spark()
                .drop_duplicates(self.join_keys)
                .limit(limit)
                .toPandas()
            )
        except AnalysisException as e:
            if "Path does not exist:" in e.desc:
                raise errors.FD_PREVIEW_NO_MATERIALIZED_OFFLINE_DATA
            else:
                raise e

        if len(pandas_df) == 0:
            # spine_time_limits refers to the range of feature timestamps. Converting to the corresponding raw data time range.
            raw_data_time_limits = aggregations._get_time_limits(
                fpov=FeaturePackageOrView.of(self._proto), spine_df=None, spine_time_limits=time_range
            )
            time_range_type = "default" if time_range is None else "provided"
            logger.warn(
                f"No preview data could be generated because no data was found in the {time_range_type} "
                f"time range of {raw_data_time_limits}. To specify a different time range, set the parameter 'time_range'"
            )
        return tecton.interactive.data_frame.set_pandas_timezone_from_spark(pandas_df)

    def _assert_writes_to_offline_feature_store(self):
        if not self._writes_to_offline_feature_store:
            raise errors.FP_NEEDS_TO_BE_MATERIALIZED(self.name)

    @sdk_public_method
    def get_feature_dataframe(
        self,
        spine: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, None] = None,
        spine_time_key: str = None,
        use_materialized_data: bool = True,
        save: bool = None,
        save_as: str = None,
    ) -> "tecton.interactive.data_frame.DataFrame":
        """
        Returns a Tecton :class:`DataFrame` that contains the output Feature Transformation of the Feature View.

        :param spine: (Optional) The spine to join against, as a dataframe.
            If present, the returned data frame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine. If spine is not
            specified, it'll return a dataframe with sample feature vectors.
        :param spine_time_key: (Optional) Name of the time column in spine.
            If unspecified, will default to the time column of the spine if there is only one present.
        :param use_materialized_data: (Optional) Use materialized data if materialization is enabled
        :param save: (Optional) set to True to persist DataFrame as a Dataset object
        :param save_as: (Optional) name to save the DataFrame as. Not applicable when save=False.
            If unspecified and save=True, a name will be generated.
        :return: A Tecton :class:`DataFrame`.
        """
        from tecton.tecton_context import TectonContext

        tc = TectonContext.get_instance()
        # TODO: be able to use self._get_feature_dataframe_with_limits directly
        # doing it this way for now to return timestamps provided by user rather than anchor times

        if self.is_online and spine is None:
            raise errors.FP_GET_FEATURE_DF_NO_SPINE

        if use_materialized_data and not self.is_online and not self._proto.materialization_enabled:
            raise errors.FD_GET_FEATURES_FROM_DISABLED_MATERIALIZATION(self.name, self.workspace)

        TectonContext.validate_spine_type(spine)

        timestamp_key = spine_time_key
        if self._should_infer_timestamp_of_spine(timestamp_key, spine):
            timestamp_key = utils.infer_timestamp(spine)

        feature_set_config = self._construct_feature_set_config()
        df = tc.execute(
            spine,
            feature_set_config=feature_set_config,
            timestamp_key=timestamp_key,
            use_materialized_data=use_materialized_data,
        )
        if save or save_as is not None:
            return Dataset._create(
                df=df,
                save_as=save_as,
                workspace=self.workspace,
                feature_package_id=self.id,
                spine=spine,
                timestamp_key=timestamp_key,
            )
        return df

    @sdk_public_method
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        timestamp_key: str = None,
        start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        entities: Optional[Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> TectonDataFrame:
        """
        Returns a Tecton :class:`DataFrame` of historical values for this feature view.
        If no arguments are passed in, all feature values for this feature view will be returned in a Tecton DataFrame.
        Note:
        The ``timestamp_key`` parameter is only applicable when a spine is passed in.
        Parameters ``start_time`, ``end_time``, and ``entities`` are only applicable when a spine is not passed in.

        :param spine: (Optional) The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
           To distinguish between spine columns and feature columns, feature columns are labeled as
            ``feature_view_name.feature_name`` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :param timestamp_key: (Optional) Name of the time column in spine.
            If unspecified, will default to the time column of the spine if there is only one present.
        :param start_time: (Optional) The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :param end_time: (Optional) The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :param entities: (Optional) Filter feature data returned to a set of entity IDs.
            If specified, this DataFrame should only contain join key columns.
        :param from_source: (Optional) Whether feature values should be recomputed from the original data source.
            If False, we will read the values from the materialized store.
        :param save: (Optional) set to True to persist DataFrame as a Dataset object. Default is False.
        :param save_as: (Optional) name to save the DataFrame as.
            If unspecified and save=True, a name will be generated.
        :return: A Tecton :class:`DataFrame`.
        """
        return self._get_historical_features(
            spine, timestamp_key, start_time, end_time, entities, from_source, save, save_as
        )

    def _upload_df_spark(self, df_path: str, df: pyspark.sql.dataframe.DataFrame):
        df.write.parquet(df_path)

    @property
    def timestamp_key(self) -> Optional[str]:
        """
        Returns the timestamp_key column name of this FeatureView.
        """
        if self._proto.HasField("timestamp_key"):
            return self._proto.timestamp_key
        return None

    # TODO(raviphol): migrate this to subclasses
    @property
    def is_temporal_aggregate(self):
        """
        Returns whether or not this FeatureView is of type TemporalAggregateFeatureView.
        """
        return self._proto.HasField("temporal_aggregate")

    # TODO(raviphol): migrate this to subclasses
    @property
    def is_temporal(self):
        """
        Returns whether or not this FeatureView is of type TemporalFeatureView.
        """
        return self._proto.HasField("temporal")

    # TODO(raviphol): migrate this to subclasses
    @property
    def is_online(self):
        """
        Returns whether or not this FeatureView is of type OnDemandFeatureView.
        """
        return self._proto.HasField("on_demand_feature_view")

    @property
    def _writes_to_offline_feature_store(self) -> bool:
        """
        Returns if the FeatureView materialization is enabled to write to the OfflineStore.
        Return value does not reflect the completion of any specific materialization job.
        """
        return self._proto.materialization_enabled and self._proto.materialization_params.writes_to_offline_store

    @property
    def _writes_to_online_feature_store(self) -> bool:
        """
        Returns if the FeatureView materialization is enabled to write to the OnlineStore.
        Return value does not reflect the completion of any specific materialization job.
        """
        return self._proto.materialization_enabled and self._proto.materialization_params.writes_to_online_store

    @property
    def _materialization_params(self) -> Optional[MaterializationParams]:
        return MaterializationParams.from_proto(self._proto)

    @property  # type: ignore
    @sdk_public_method
    def feature_start_time(self) -> Optional[pendulum.DateTime]:
        """
        This represents the time at which features are first available.
        """
        if not self._proto.HasField("materialization_params"):
            return None
        return pendulum.from_timestamp(self._proto.materialization_params.start_timestamp.ToSeconds())

    @property  # type: ignore
    @sdk_public_method
    def batch_materialization_schedule(self) -> Optional[pendulum.Duration]:
        """
        This represents how often we schedule batch materialization jobs.
        """
        if not self._proto.HasField("materialization_params"):
            return None
        # TODO: this should return a formatted duration, not a timestamp
        return pendulum.Duration(seconds=self._proto.materialization_params.schedule_interval.ToSeconds())

    @property  # type: ignore
    @sdk_public_method
    def schedule_offset(self) -> Optional[pendulum.Duration]:
        """
        If this attribute is non-empty, Tecton will schedule materialization jobs at an offset equal to this.
        """
        if not self._proto.HasField("materialization_params"):
            return None
        schedule_offset = pendulum.duration(
            seconds=self._proto.materialization_params.allowed_upstream_lateness.ToSeconds()
        )
        if not schedule_offset:
            return None
        return schedule_offset

    @property  # type: ignore
    @sdk_public_method
    def type(self):
        """
        Returns the FeatureView type.
        """
        if self.is_temporal:
            return "Temporal"
        elif self.is_temporal_aggregate:
            return "TemporalAggregate"
        elif self.is_online:
            return "OnDemand"
        else:
            # Should never happen
            raise errors.INTERNAL_ERROR(f"Invalid feature type for FeatureView {self.name}")

    @sdk_public_method
    def get_features(
        self,
        entities: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, None] = None,
        start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        from_source: bool = False,
    ) -> "tecton.interactive.data_frame.DataFrame":
        """
        Returns all the feature values that are defined by this Feature View in the specified time range.

        :param entities: (Optional) Filter feature data to a set of entity IDs.
            If specified, this DataFrame should only contain join key columns.
        :param start_time: (Optional) The interval start time from when we want to retrieve features.
        :param end_time:  (Optional) The interval end time until when we want to retrieve features.
        :param from_source: Whether feature values should be recomputed from the original data source.
            If False, we will attempt to read the values from the materialized store.

        :return: A Tecton DataFrame with features values.
        """

        fpov = FeaturePackageOrView.of(self._proto)

        return feature_retrieval_internal.get_features(fpov, entities, start_time, end_time, from_source)

    @sdk_public_method
    def get_feature_vector(
        self,
        join_keys: Optional[Mapping[str, Union[int, np.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_context_map: Optional[Mapping[str, Union[int, np.int_, str, bytes, float]]] = None,
    ) -> FeatureVector:
        """
        Returns a single Tecton :class:`FeatureVector` from the Online Store.
        At least one of join_keys or request_context_map is required.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_context_map: Dictionary of request context values.

        :return: A :class:`FeatureVector` of the results.
        """
        # doing checks here instead of get_online_features in order to provide the correct error messages
        if not self._writes_to_online_feature_store and not self.is_online:
            raise errors.UNSUPPORTED_OPERATION(
                "get_feature_vector", "online_serving_enabled is not set to True for this FeatureView."
            )
        if join_keys is None and request_context_map is None:
            raise errors.FS_GET_FEATURE_VECTOR_REQUIRED_ARGS
        if self.is_online:
            # validate request_context_map
            required_request_context_keys = list(self._request_context.arg_to_schema.keys())
            if len(required_request_context_keys) > 0 and request_context_map is None:
                raise errors.GET_FEATURE_VECTOR_FV_NO_REQUEST_DATA(required_request_context_keys)
            utils.validate_request_data(request_context_map, required_request_context_keys, is_read_api_v3=False)
            # check if we need join keys
            if join_keys is None and utils.get_num_dependent_fv(self._proto.pipeline.root, visited_inputs={}) > 0:
                raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS
            return self.get_online_features(join_keys, include_join_keys_in_response, request_context_map)
        return self.get_online_features(join_keys, include_join_keys_in_response)

    @sdk_public_method
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """
        Returns a single Tecton :class:`FeatureVector` from the Online Store.
        At least one of join_keys or request_data is required.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_data: Dictionary of request context values.

        :return: A :class:`FeatureVector` of the results.
        """
        if not self._writes_to_online_feature_store:
            raise errors.UNSUPPORTED_OPERATION(
                "get_online_features", "online_serving_enabled is not set to True for this FeatureView."
            )
        utils.validate_join_key_types(join_keys)

        return _QueryHelper(self._proto.fco_metadata.workspace, feature_package_name=self.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            {},
            self._request_context,
        )

    @property
    def _request_context(self) -> Optional[RequestContext]:
        return RequestContext({})

    @property
    def _materialization_schema(self):
        from tecton_spark.schema import Schema

        return Schema(self._proto.schemas.materialization_schema)


def is_documented_by(original):
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


class BatchWindowAggregateFeatureView(FeatureView):
    """
    BatchWindowAggregateFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    def run(
        self,
        feature_start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        feature_end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        aggregate_tiles: bool = True,
        **mock_inputs: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.DataFrame":
        """
        Run the FeatureView on the fly. It supports mock input data, but if mock_inputs is not provided for some
        features, those inputs will be retrieved from the linked DataSources. In that case, the run may takes several
        minutes to retrieve the data.

        :param feature_start_time: Start time for the feature. mock_inputs and linked DataSources will be filtered in
            respect to providing neccessity inputs for this feature time.
            The output values with timestamps earlier than this will be dropped.

        :param feature_end_time: End time for input data (both data sources, and mock_inputs). mock_inputs and linked
            DataSources will be filtered in respect to providing neccessity inputs for this feature time.
            The output values with timestamps later than this will be dropped.

        :param aggregate_tiles: Only available for BatchWindowAggregateFeatureView and StreamWindowAggregateFeatureView.
            Enables within-tile aggregation, and outputs event-level features.

        :param \*\*mock_inputs: If provided, mock_inputs will be used as the FeatureView inputs for the Run, instead of
            the data from linked DataSources. The name of the parameter(s) must be a valid FeatureView input names.

        Example:
            A FeatureView 'fv' with inputs: 'ds1', 'ds2'.

            1) :py:func:`fv.run()` Use inputs from the linked DataSources for both ds1 and ds2.

            2) :py:func:`fv.run(ds1=mock_dataframe1)` Use mock_dataframe1 as input ds1, ds2 from a linked DataSource.

            3) :py:func:`fv.run(ds1=mock_dataframe1, ds2=mock_dataframe2)` Use the mock dataframes for both ds1 and ds2.

        :return: A tecton DataFrame of the results.
        """
        return run_batch(self._proto, feature_start_time, feature_end_time, mock_inputs, aggregate_tiles)


class BatchFeatureView(FeatureView):
    """
    BatchFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    @is_documented_by(BatchWindowAggregateFeatureView.run)
    def run(
        self,
        feature_start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        feature_end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        **mock_inputs: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.DataFrame":
        return run_batch(self._proto, feature_start_time, feature_end_time, mock_inputs)


class StreamFeatureView(FeatureView):
    """
    StreamFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    @is_documented_by(BatchFeatureView.run)
    def run(
        self,
        feature_start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        feature_end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        **mock_inputs: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.DataFrame":
        return run_batch(self._proto, feature_start_time, feature_end_time, mock_inputs)

    @sdk_public_method
    def run_stream(self, output_temp_table: str) -> None:
        """
        Starts a streaming job to keep writting the output records of this FeatureView to a temporary table.
        The job will be running until the execution is terminated.

        After records have been written to the table, they can be queried using `spark.sql()`.
        If ran in a Databricks notebook, Databricks will also automatically visualize the number of incoming records.

        :param output_temp_table: The name of the temporary table to write to.

        Example:

            1) :py:func:`fv.run_stream(output_temp_table="temp_table")` Start a streaming job.

            2) :py:func:`display(spark.sql("SELECT * FROM temp_table LIMIT 5"))` Query the output table, and display the output dataframe.
        """
        return run_stream(self._proto, output_temp_table)


class StreamWindowAggregateFeatureView(FeatureView):
    """
    StreamFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    @is_documented_by(BatchWindowAggregateFeatureView.run)
    def run(
        self,
        feature_start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        feature_end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
        aggregate_tiles: bool = True,
        **mock_inputs: Union[pandas.DataFrame, DataFrame],
    ) -> "tecton.interactive.data_frame.DataFrame":
        return run_batch(self._proto, feature_start_time, feature_end_time, mock_inputs, aggregate_tiles)

    @sdk_public_method
    @is_documented_by(StreamFeatureView.run_stream)
    def run_stream(self, output_temp_table: str) -> None:
        return run_stream(self._proto, output_temp_table)


class OnDemandFeatureView(FeatureView):
    """
    OnDemandFeatureView class.

    To get a FeatureView instance, call :py:func:`tecton.get_feature_view`.
    """

    @sdk_public_method
    def run(self, **mock_inputs: Union[pandas.DataFrame, DataFrame]) -> "tecton.interactive.data_frame.DataFrame":
        """
        Run the OnDemandFeatureView using the specified mock_inputs.

        :param mock_inputs: It must contain all the inputs required by the FeatureView. All dataframes must contain
            the same number of rows and their matching row ordering.

        :return: A tecton DataFrame of the results.
        """
        return run_ondemand(self._proto, self.name, mock_inputs)

    def _online_transform_dataframe(
        self,
        spine: DataFrame,
        use_materialized_data: bool = True,
        namespace: Optional[str] = None,
    ) -> DataFrame:
        """
        Adds features from an OnDemandFeatureView to the spine.

        :param spine: Spark dataframe used to compute the on-demand features. Any dependent feature values must already be a part of the spine.
        :param use_materialized_data: (Optional) Use materialized data if materialization is enabled.

        :return: A spark dataframe containing the spine augmented with features. The features are prefixed by the namespace if it exists, or the FeatureView's name.
        """
        df = pipeline_helper.dataframe_with_input(
            pipeline=self._proto.pipeline,
            spark=TectonContext.get_instance()._spark,
            input_df=spine,
            output_schema=self._materialization_schema.to_spark(),
            transformations=self._proto.enrichments.transformations,
            name=self.name,
            fv_id=self.id,
            namespace=namespace,
        )
        return df

    def _should_infer_timestamp_of_spine(
        self, timestamp_key: Optional[str], spine: Optional[Union[pandas.DataFrame, DataFrame]]
    ):
        if timestamp_key is not None:
            return False
        if spine is None:
            return False
        # normally odfvs don't depend on a timestamp key except for when they have dependent fvs
        # in this case we want to infer the timestamp key of the spine. A dependent fv can't be a odfv.
        return utils.get_num_dependent_fv(self._proto.pipeline.root, visited_inputs={}) > 0

    @sdk_public_method
    def get_historical_features(
        self,
        spine: Union[pyspark.sql.dataframe.DataFrame, pandas.DataFrame, TectonDataFrame] = None,
        timestamp_key: str = None,
        from_source: bool = False,
        save: bool = False,
        save_as: Optional[str] = None,
    ) -> TectonDataFrame:
        """
        Returns a Tecton :class:`DataFrame` of historical values for this feature view.

        :param spine: The spine to join against, as a dataframe.
            The returned data frame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine. If spine is not
            specified, it'll return a dataframe of  feature values in the specified time range.
        :param timestamp_key: (Optional) Name of the time column in spine.
            If unspecified, will default to the time column of the spine if there is only one present.
        :param from_source: (Optional) Whether feature values should be recomputed from the original data source.
            If False, we will read the values from the materialized store.
        :param save: (Optional) Set to True to persist DataFrame as a Dataset object. Default value is False.
        :param save_as: (Optional) name to save the DataFrame as.If unspecified and save=True, a name will be generated.
        :return: A Tecton :class:`DataFrame`.
        """
        return self._get_historical_features(
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=None,
            end_time=None,
            entities=None,
            from_source=from_source,
            save=save,
            save_as=save_as,
        )

    @sdk_public_method
    def get_online_features(
        self,
        join_keys: Optional[Mapping[str, Union[int, np.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_data: Optional[Mapping[str, Union[int, np.int_, str, bytes, float]]] = None,
    ) -> FeatureVector:
        """
        Returns a single Tecton :class:`FeatureVector` from the Online Store.
        At least one of join_keys or request_data is required.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_data: Dictionary of request context values used for OnDemand Feature Views.

        :return: A :class:`FeatureVector` of the results.
        """
        if join_keys is None and request_data is None:
            raise errors.GET_ONLINE_FEATURES_REQUIRED_ARGS
        if join_keys is None and utils.get_num_dependent_fv(self._proto.pipeline.root, visited_inputs={}) > 0:
            raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS
        if join_keys is not None:
            utils.validate_join_key_types(join_keys)
        if request_data is not None and not isinstance(request_data, dict):
            raise errors.INVALID_REQUEST_DATA_TYPE(type(request_data))

        required_request_context_keys = list(self._request_context.arg_to_schema.keys())
        if len(required_request_context_keys) > 0 and request_data is None:
            raise errors.GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(required_request_context_keys)
        utils.validate_request_data(request_data, required_request_context_keys)

        return _QueryHelper(self._proto.fco_metadata.workspace, feature_package_name=self.name).get_feature_vector(
            join_keys or {},
            include_join_keys_in_response,
            request_data or {},
            self._request_context,
        )

    @property
    def _request_context(self) -> Optional[RequestContext]:
        rc = find_request_context(self._proto.pipeline.root)
        return RequestContext({}) if rc is None else RequestContext._from_proto(rc)


@sdk_public_method
def get_feature_view(fv_reference: str, workspace_name: Optional[str] = None) -> FeatureView:
    """
    Fetch an existing :class:`FeatureView` by name.

    :param fv_reference: Either a name or a hexadecimal Feature View ID.
    :returns: :class:`BatchFeatureView`, :class:`BatchWindowAggregateFeatureView`,
        :class:`StreamFeatureView`, :class:`StreamWindowAggregateFeatureView`,
        or :class:`OnDemandFeatureView`.
    """
    request = GetFeatureViewRequest()
    request.version_specifier = fv_reference
    request.workspace = workspace_name or conf.get_or_none("TECTON_WORKSPACE")
    response = metadata_service.instance().GetFeatureView(request)
    if not response.HasField("feature_view"):
        raise errors.FCO_NOT_FOUND(FeatureView, fv_reference)

    if response.feature_view.HasField("feature_table"):
        raise errors.FCO_NOT_FOUND_WRONG_TYPE(FeatureView, fv_reference, "get_feature_table")

    return _get_feature_view_by_type(response.feature_view, fv_reference)


def _get_feature_view_by_type(feature_view_proto: feature_view_pb2.FeatureView, fv_reference: str):
    if feature_view_proto.HasField("on_demand_feature_view"):
        return OnDemandFeatureView(feature_view_proto)
    if feature_view_proto.HasField("temporal"):
        data_source_type = feature_view_proto.temporal.data_source_type
        if data_source_type == DataSourceType.BATCH:
            return BatchFeatureView(feature_view_proto)
        if data_source_type == DataSourceType.STREAM_WITH_BATCH:
            return StreamFeatureView(feature_view_proto)
        raise errors.INTERNAL_ERROR("Missing data_source_type for temporal FeatureView.")
    if feature_view_proto.HasField("temporal_aggregate"):
        data_source_type = feature_view_proto.temporal_aggregate.data_source_type
        if data_source_type == DataSourceType.BATCH:
            return BatchWindowAggregateFeatureView(feature_view_proto)
        if data_source_type == DataSourceType.STREAM_WITH_BATCH:
            return StreamWindowAggregateFeatureView(feature_view_proto)
        raise errors.INTERNAL_ERROR("Missing data_source_type for temporal aggregate FeatureView.")
    raise errors.INTERNAL_ERROR("Missing or unsupported FeatureView type.")
