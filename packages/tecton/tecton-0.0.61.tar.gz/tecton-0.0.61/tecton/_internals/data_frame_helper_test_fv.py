from unittest import TestCase
from unittest.mock import patch

import pandas
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType

import tecton.interactive
from tecton import RequestContext
from tecton._internals import data_frame_helper
from tecton.interactive.feature_set_config import FeatureSetConfig
from tecton_proto.args.new_transformation_pb2 import TransformationMode
from tecton_proto.args.pipeline_pb2 import Input
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineMode
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import RequestDataSourceNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.common.aggregation_function_pb2 import AggregationFunction
from tecton_proto.data import feature_package_pb2
from tecton_proto.data.feature_package_pb2 import OnlineServingIndex
from tecton_proto.data.feature_store_pb2 import FeatureStoreFormatVersion
from tecton_proto.data.feature_types_pb2 import AggregateFeature as AggregateFeatureProto
from tecton_proto.data.feature_view_pb2 import FeatureView
from tecton_proto.data.feature_view_pb2 import NewTemporal
from tecton_proto.data.feature_view_pb2 import NewTemporalAggregate
from tecton_proto.data.feature_view_pb2 import OnDemandFeatureView
from tecton_proto.data.new_transformation_pb2 import NewTransformation
from tecton_spark import function_serialization as func_ser
from tecton_spark.feature_package_view import FeaturePackageOrView
from tecton_spark.id_helper import IdHelper
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.schema import Schema
from testing.tecton_context import testing_spark_context
from testing.tecton_context import testing_tecton_context

pandas.set_option("display.max_columns", None)
pandas.set_option("display.max_rows", None)


def transformationFuntion():
    return f"""
    SELECT
        *
    FROM
        logs
    """


class DataFrameHelperTest(TestCase):
    Ctx = None
    spark = None

    @classmethod
    def setup_class(cls):
        cls.Ctx = testing_tecton_context()
        cls.spark = testing_spark_context()

    def _get_spark_df(self, columns, data, timestamp_column=None):
        df = self.spark.createDataFrame(data, columns)
        if timestamp_column is not None:
            df = df.withColumn(timestamp_column, col(timestamp_column).cast("timestamp"))
        return df

    def _create_spine(self):
        return self._get_spark_df(
            ["A", "B", "timestamp"],
            [
                [1, 1, "2018-10-30T15:01:00Z"],
                [1, 2, "2018-10-30T15:01:00Z"],
                [3, 3, "2018-10-30T15:01:00Z"],
                [10, 10, "2018-10-30T15:01:00Z"],
                [1, 1, "2018-10-30T13:01:00Z"],
                [1, 2, "2018-10-30T13:01:00Z"],
                [3, 3, "2018-10-30T13:01:00Z"],
            ],
            "timestamp",
        )

    def _create_id(self):
        return IdHelper.from_string(IdHelper.generate_string_id())

    def _create_transformation(
        self, transformation_function, transformation_mode=TransformationMode.TRANSFORMATION_MODE_SPARK_SQL
    ):
        transform = NewTransformation()
        transform.transformation_id.CopyFrom(self._create_id())
        transform.fco_metadata.name = "transformation"
        transform.fco_metadata.description = "test fv"
        transform.transformation_mode = transformation_mode
        transform.user_function.CopyFrom(func_ser.to_proto(func_ser.inlined(transformation_function), DataFrame))
        return transform

    def _create_pipeline(self, transformation_id) -> Pipeline:
        pipeline = Pipeline()

        transformation_node = TransformationNode()
        transformation_node.transformation_id.CopyFrom(transformation_id)
        transformation_pipeline_node = PipelineNode()

        transformation_input = Input()
        transformation_input.arg_index = 0
        transformation_node.inputs.append(transformation_input)

        transformation_pipeline_node.transformation_node.CopyFrom(transformation_node)

        pipeline.root.CopyFrom(transformation_pipeline_node)
        pipeline.mode = PipelineMode.PIPELINE_MODE_SPARK
        return pipeline

    def _create_TAFV(self, fv_name, bound_keys=[], wildcard_keys=[]):
        transformation = self._create_transformation(transformationFuntion)
        feature_view = self._create_aggregate_feature_view(fv_name, transformation, bound_keys, wildcard_keys)
        return tecton.interactive.FeatureView(feature_view)

    def _create_aggregate_feature_view(
        self, name, transformation: NewTransformation, bound_keys, wildcard_keys
    ) -> FeatureView:
        feature_view_proto = FeatureView()
        feature_view_proto.fco_metadata.name = name
        feature_view_proto.materialization_params.schedule_interval.seconds = 3600

        new_temporal_aggregate = NewTemporalAggregate()

        feature = AggregateFeatureProto()
        feature.input_feature_name = "score"
        feature.output_feature_name = "score_count_3hours_1h"
        feature.function = AggregationFunction.AGGREGATION_FUNCTION_COUNT
        feature.window.seconds = 3 * 60 * 60  # 3 hours in seconds
        new_temporal_aggregate.features.append(feature)

        new_temporal_aggregate.slide_interval.FromSeconds(3600)
        new_temporal_aggregate.is_continuous = False

        feature_view_proto.temporal_aggregate.CopyFrom(new_temporal_aggregate)

        pipeline = self._create_pipeline(transformation.transformation_id)
        feature_view_proto.pipeline.CopyFrom(pipeline)

        feature_view_proto.join_keys.extend(bound_keys + wildcard_keys)

        index = OnlineServingIndex()
        index.join_keys.extend(bound_keys)
        feature_view_proto.online_serving_index.CopyFrom(index)

        feature_view_proto.schemas.view_schema.columns.add().name = "score"
        feature_view_proto.enrichments.transformations.append(transformation)
        feature_view_proto.timestamp_key = "timestamp"
        feature_view_proto.feature_store_format_version = FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT

        return feature_view_proto

    def _create_feature_view(self, name, transformation: NewTransformation, bound_keys, wildcard_keys) -> FeatureView:
        feature_view_proto = FeatureView()
        feature_view_proto.fco_metadata.name = name
        feature_view_proto.materialization_params.schedule_interval.seconds = 3600

        new_temporal = NewTemporal()
        new_temporal.serving_ttl.FromSeconds(3 * 3600)

        pipeline = self._create_pipeline(transformation.transformation_id)

        feature_view_proto.temporal.CopyFrom(new_temporal)
        feature_view_proto.pipeline.CopyFrom(pipeline)

        feature_view_proto.join_keys.extend(bound_keys + wildcard_keys)

        index = OnlineServingIndex()
        index.join_keys.extend(bound_keys)
        feature_view_proto.online_serving_index.CopyFrom(index)

        feature_view_proto.schemas.view_schema.columns.add().name = "score"
        feature_view_proto.enrichments.transformations.append(transformation)
        feature_view_proto.timestamp_key = "timestamp"
        feature_view_proto.feature_store_format_version = FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT

        return feature_view_proto

    def _create_TFV(self, fv_name, bound_keys=[], wildcard_keys=[]):
        transformation = self._create_transformation(transformationFuntion)
        feature_view = self._create_feature_view(fv_name, transformation, bound_keys, wildcard_keys)
        return tecton.interactive.FeatureView(feature_view)

    def _run_test_fetching_training_data_TAFV(self, fv, get_materialized_tiles):
        fsc = tecton.interactive.feature_set_config.FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(fv._proto))

        tiles = [
            [1, 1, "2018-10-30T10:00:00Z", 10],
            [1, 1, "2018-10-30T12:00:00Z", 30],
            [1, 1, "2018-10-30T14:00:00Z", 40],
            [1, 2, "2018-10-30T11:00:00Z", 20],
            [1, 2, "2018-10-30T13:00:00Z", 40],
            [1, 2, "2018-10-30T15:00:00Z", 60],
            [3, 3, "2018-10-30T10:00:00Z", 10],
            [3, 3, "2018-10-30T15:00:00Z", 60],
        ]
        materialized_tiles = self._get_spark_df(["A", "B", "timestamp", "count_score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )
        get_materialized_tiles.return_value = materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "timestamp", "tafv.score_count_3hours_1h"],
                [
                    [1, 1, "2018-10-30T15:01:00Z", 70],
                    [1, 2, "2018-10-30T15:01:00Z", 40],
                    [3, 3, "2018-10-30T15:01:00Z", 0],
                    [10, 10, "2018-10-30T15:01:00Z", 0],
                    [1, 1, "2018-10-30T13:01:00Z", 40],
                    [1, 2, "2018-10-30T13:01:00Z", 20],
                    [3, 3, "2018-10-30T13:01:00Z", 10],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__bound_TAFV(self, get_materialized_tiles):
        fv = self._create_TAFV("tafv", ["A", "B"])
        self._run_test_fetching_training_data_TAFV(fv, get_materialized_tiles)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__wildcard_TAFV_with_all_keys_passed(self, get_materialized_tiles):
        fv = self._create_TAFV("tafv", ["A"], ["B"])
        self._run_test_fetching_training_data_TAFV(fv, get_materialized_tiles)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__wildcard_TAFV(self, get_materialized_tiles):
        fv = self._create_TAFV("tafv", ["A", "B"], ["C"])
        fsc = FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(fv._proto))

        tiles = [
            [1, 1, "X", "2018-10-30T10:00:00Z", 10],
            [1, 1, "X", "2018-10-30T12:00:00Z", 30],
            [1, 1, "Y", "2018-10-30T14:00:00Z", 40],
            [1, 2, "X", "2018-10-30T11:00:00Z", 20],
            [1, 2, "X", "2018-10-30T13:00:00Z", 40],
            [1, 2, "Y", "2018-10-30T14:00:00Z", 60],
            [3, 3, "Z", "2018-10-30T10:00:00Z", 10],
            [3, 3, "Z", "2018-10-30T15:00:00Z", 60],
        ]
        materialized_tiles = self._get_spark_df(
            ["A", "B", "C", "timestamp", "count_score"], tiles, "timestamp"
        ).withColumn(TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp"))
        get_materialized_tiles.return_value = materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "C", "timestamp", "tafv.score_count_3hours_1h"],
                [
                    [1, 1, "X", "2018-10-30T15:01:00Z", 30],
                    [1, 1, "Y", "2018-10-30T15:01:00Z", 40],
                    [1, 2, "X", "2018-10-30T15:01:00Z", 40],
                    [1, 2, "Y", "2018-10-30T15:01:00Z", 60],
                    [3, 3, None, "2018-10-30T15:01:00Z", None],
                    [10, 10, None, "2018-10-30T15:01:00Z", None],
                    [1, 1, "X", "2018-10-30T13:01:00Z", 40],
                    [1, 2, "X", "2018-10-30T13:01:00Z", 20],
                    [3, 3, "Z", "2018-10-30T13:01:00Z", 10],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__bound_and_wildcard_TAFVs(self, get_materialized_tiles):
        bound_fv = self._create_TAFV("bound_tafv", ["A", "B"])
        wildcard_fv = self._create_TAFV("wildcard_tafv", ["A", "B"], ["C"])
        fsc = FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(wildcard_fv._proto))
        fsc._add(FeaturePackageOrView.of(bound_fv._proto))

        tiles = [
            [1, 1, "2018-10-30T10:00:00Z", 10],
            [1, 1, "2018-10-30T13:00:00Z", 20],
            [1, 1, "2018-10-30T20:00:00Z", 30],
            [1, 2, "2018-10-30T11:00:00Z", 40],
            [1, 2, "2018-10-30T14:00:00Z", 50],
            [3, 3, "2018-10-30T10:00:00Z", 60],
            [4, 4, "2018-10-30T14:00:00Z", 70],
        ]
        bound_tiles = self._get_spark_df(["A", "B", "timestamp", "count_score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        tiles = [
            [1, 1, "X", "2018-10-30T10:00:00Z", 11],
            [1, 1, "X", "2018-10-30T12:00:00Z", 22],
            [1, 1, "Y", "2018-10-30T14:00:00Z", 33],
            [1, 2, "X", "2018-10-30T13:00:00Z", 44],
            [1, 2, "Y", "2018-10-30T14:00:00Z", 55],
            [3, 3, "Z", "2018-10-30T14:00:00Z", 66],
        ]
        wildcard_tiles = self._get_spark_df(["A", "B", "C", "timestamp", "count_score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        def _mock_get_materialized_tiles(tc, fv, use_materialized_data, spine_time_limits):
            return bound_tiles if fv.name == "bound_tafv" else wildcard_tiles

        get_materialized_tiles.side_effect = _mock_get_materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "C", "timestamp", "bound_tafv.score_count_3hours_1h", "wildcard_tafv.score_count_3hours_1h"],
                [
                    [1, 1, "X", "2018-10-30T15:01:00Z", 20, 22],
                    [1, 1, "Y", "2018-10-30T15:01:00Z", 20, 33],
                    [1, 2, "X", "2018-10-30T15:01:00Z", 50, 44],
                    [1, 2, "Y", "2018-10-30T15:01:00Z", 50, 55],
                    [3, 3, "Z", "2018-10-30T15:01:00Z", 0, 66],
                    [10, 10, None, "2018-10-30T15:01:00Z", 0, None],
                    [1, 1, "X", "2018-10-30T13:01:00Z", 10, 33],
                    [1, 2, None, "2018-10-30T13:01:00Z", 40, None],
                    [3, 3, None, "2018-10-30T13:01:00Z", 60, None],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__multiple_wildcard_TAFVs(self, get_materialized_tiles):
        wildcard_fv_1 = self._create_TAFV("wildcard_tafv_1", ["A", "B"], ["C"])
        wildcard_fv_2 = self._create_TAFV("wildcard_tafv_2", ["A"], ["C"])
        wildcard_fv_3 = self._create_TAFV("wildcard_tafv_3", ["B"], ["C"])
        fsc = tecton.interactive.feature_set_config.FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(wildcard_fv_2._proto))
        fsc._add(FeaturePackageOrView.of(wildcard_fv_1._proto))
        fsc._add(FeaturePackageOrView.of(wildcard_fv_3._proto))

        tiles = [
            [1, 1, "Y", "2018-10-30T10:00:00Z", 11],
            [1, 1, "Z", "2018-10-30T11:00:00Z", 21],
            [1, 2, "X", "2018-10-30T10:00:00Z", 31],
            [1, 2, "X", "2018-10-30T11:00:00Z", 41],
            [1, 1, "Y", "2018-10-30T14:00:00Z", 51],
            [3, 3, "Z", "2018-10-30T14:00:00Z", 61],
        ]
        wildcard_fv_tiles_1 = self._get_spark_df(
            ["A", "B", "C", "timestamp", "count_score"], tiles, "timestamp"
        ).withColumn(TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp"))

        tiles = [
            [1, "X", "2018-10-30T10:00:00Z", 12],
            [1, "Y", "2018-10-30T11:00:00Z", 22],
            [3, "Z", "2018-10-30T10:00:00Z", 42],
            [1, "X", "2018-10-30T13:00:00Z", 52],
        ]
        wildcard_fv_tiles_2 = self._get_spark_df(["A", "C", "timestamp", "count_score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        tiles = [
            [1, "X", "2018-10-30T10:00:00Z", 13],
            [1, "Y", "2018-10-30T11:00:00Z", 23],
            [1, "T", "2018-10-30T11:00:00Z", 33],
            [2, "X", "2018-10-30T14:00:00Z", 43],
            [3, "Z", "2018-10-30T10:00:00Z", 53],
            [3, "T", "2018-10-30T11:00:00Z", 63],
            [3, "Z", "2018-10-30T13:00:00Z", 73],
            [1, "Z", "2018-10-30T14:00:00Z", 83],
        ]
        wildcard_fv_tiles_3 = self._get_spark_df(["B", "C", "timestamp", "count_score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        def _mock_get_materialized_tiles(tc, fv, use_materialized_data, spine_time_limits):
            if fv.name == "wildcard_tafv_1":
                return wildcard_fv_tiles_1
            if fv.name == "wildcard_tafv_2":
                return wildcard_fv_tiles_2
            return wildcard_fv_tiles_3

        get_materialized_tiles.side_effect = _mock_get_materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                [
                    "A",
                    "B",
                    "C",
                    "timestamp",
                    "wildcard_tafv_1.score_count_3hours_1h",
                    "wildcard_tafv_2.score_count_3hours_1h",
                    "wildcard_tafv_3.score_count_3hours_1h",
                ],
                [
                    [1, 1, "X", "2018-10-30T13:01:00Z", None, 12, 13],
                    [1, 1, "Y", "2018-10-30T13:01:00Z", 11, 22, 23],
                    [1, 1, "Z", "2018-10-30T13:01:00Z", 21, None, None],
                    [1, 1, "T", "2018-10-30T13:01:00Z", None, None, 33],
                    [1, 2, "X", "2018-10-30T13:01:00Z", 31 + 41, 12, None],
                    [1, 2, "Y", "2018-10-30T13:01:00Z", None, 22, None],
                    [3, 3, "Z", "2018-10-30T13:01:00Z", None, 42, 53],
                    [3, 3, "T", "2018-10-30T13:01:00Z", None, None, 63],
                    [1, 1, "X", "2018-10-30T15:01:00Z", None, 52, None],
                    [1, 1, "Y", "2018-10-30T15:01:00Z", 51, None, None],
                    [1, 1, "Z", "2018-10-30T15:01:00Z", None, None, 83],
                    [1, 2, "X", "2018-10-30T15:01:00Z", None, 52, 43],
                    [3, 3, "Z", "2018-10-30T15:01:00Z", 61, None, 73],
                    # TODO: remove
                    [3, 3, None, "2018-10-30T15:01:00Z", None, None, None],
                    [10, 10, None, "2018-10-30T15:01:00Z", None, None, None],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.set_option("display.max_rows", None, "display.max_columns", None)
        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    def _run_test_fetching_training_data_TFV(self, fv, get_materialized_tiles):
        fsc = FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(fv._proto))

        tiles = [
            [1, 1, "2018-10-30T10:10:00Z", 10],
            [1, 1, "2018-10-30T12:10:00Z", 30],
            [1, 1, "2018-10-30T14:10:00Z", 40],
            [1, 2, "2018-10-30T11:10:00Z", 20],
            [1, 2, "2018-10-30T13:10:00Z", 40],
            [1, 2, "2018-10-30T15:01:00Z", 60],
            [3, 3, "2018-10-30T12:00:00Z", 10],
            [3, 3, "2018-10-30T15:10:00Z", 60],
        ]
        materialized_tiles = self._get_spark_df(["A", "B", "timestamp", "score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp") - 600
        )
        get_materialized_tiles.return_value = materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "timestamp", "tfv.score"],
                [
                    [1, 1, "2018-10-30T15:01:00Z", 40],
                    [1, 2, "2018-10-30T15:01:00Z", 60],
                    [3, 3, "2018-10-30T15:01:00Z", None],
                    [10, 10, "2018-10-30T15:01:00Z", None],
                    [1, 1, "2018-10-30T13:01:00Z", 30],
                    [1, 2, "2018-10-30T13:01:00Z", 20],
                    [3, 3, "2018-10-30T13:01:00Z", 10],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__bound_TFV(self, get_materialized_tiles):
        fv = self._create_TFV("tfv", ["A", "B"])
        self._run_test_fetching_training_data_TFV(fv, get_materialized_tiles)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__wildcard_TFV_with_all_keys_passed(self, get_materialized_tiles):
        fv = self._create_TFV("tfv", ["A"], ["B"])
        self._run_test_fetching_training_data_TFV(fv, get_materialized_tiles)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__wildcard_TFV(self, get_materialized_tiles):
        fv = self._create_TFV("tfv", ["A", "B"], ["C"])
        fsc = FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(fv._proto))

        tiles = [
            [1, 1, "X", "2018-10-30T10:10:00Z", 10],
            [1, 1, "X", "2018-10-30T12:00:00Z", 30],
            [1, 1, "Y", "2018-10-30T11:10:00Z", 40],
            [1, 1, "Y", "2018-10-30T14:10:00Z", 40],
            [1, 2, "X", "2018-10-30T11:10:00Z", 20],
            [1, 2, "X", "2018-10-30T13:10:00Z", 40],
            [1, 2, "Y", "2018-10-30T14:10:00Z", 60],
            [3, 3, "Z", "2018-10-30T10:00:00Z", 10],
            [3, 3, "Z", "2018-10-30T15:10:00Z", 60],
        ]
        materialized_tiles = self._get_spark_df(["A", "B", "C", "timestamp", "score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp") - 600
        )
        get_materialized_tiles.return_value = materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "C", "timestamp", "tfv.score"],
                [
                    [1, 1, "Y", "2018-10-30T15:01:00Z", 40],
                    [1, 2, "X", "2018-10-30T15:01:00Z", 40],
                    [1, 2, "Y", "2018-10-30T15:01:00Z", 60],
                    [3, 3, None, "2018-10-30T15:01:00Z", None],
                    [10, 10, None, "2018-10-30T15:01:00Z", None],
                    [1, 1, "X", "2018-10-30T13:01:00Z", 30],
                    [1, 1, "Y", "2018-10-30T13:01:00Z", 40],
                    [1, 2, "X", "2018-10-30T13:01:00Z", 20],
                    [3, 3, None, "2018-10-30T13:01:00Z", None],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.feature_packages.aggregations._get_all_partial_aggregation_tiles_df")
    def test_fetching_training_data__bound_and_wildcard_TFVs(self, get_materialized_tiles):
        bound_fv = self._create_TFV("bound_tfv", ["A", "B"])
        wildcard_fv = self._create_TFV("wildcard_tfv", ["A", "B"], ["C"])
        fsc = FeatureSetConfig()
        fsc._add(FeaturePackageOrView.of(wildcard_fv._proto))
        fsc._add(FeaturePackageOrView.of(bound_fv._proto))

        tiles = [
            [1, 1, "2018-10-30T11:00:00Z", 10],
            [1, 1, "2018-10-30T14:00:00Z", 20],
            [1, 1, "2018-10-30T20:00:00Z", 30],
            [1, 2, "2018-10-30T11:00:00Z", 40],
            [1, 2, "2018-10-30T14:00:00Z", 50],
            [3, 3, "2018-10-30T11:00:00Z", 60],
            [4, 4, "2018-10-30T14:00:00Z", 70],
        ]
        bound_tiles = self._get_spark_df(["A", "B", "timestamp", "score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        tiles = [
            [1, 1, "X", "2018-10-30T10:00:00Z", 11],
            [1, 1, "X", "2018-10-30T13:00:00Z", 22],
            [1, 1, "Y", "2018-10-30T14:00:00Z", 33],
            [1, 2, "X", "2018-10-30T14:00:00Z", 44],
            [1, 2, "Y", "2018-10-30T14:00:00Z", 55],
            [3, 3, "Z", "2018-10-30T14:00:00Z", 66],
        ]
        wildcard_tiles = self._get_spark_df(["A", "B", "C", "timestamp", "score"], tiles, "timestamp").withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME, unix_timestamp("timestamp")
        )

        def _mock_get_materialized_tiles(tc, fv, use_materialized_data, spine_time_limits):
            return bound_tiles if fv.name == "bound_tfv" else wildcard_tiles

        get_materialized_tiles.side_effect = _mock_get_materialized_tiles

        spine_df = self._create_spine()
        training_dataset = (
            data_frame_helper.get_features_for_spine(
                self.spark,
                spine_df=spine_df,
                feature_set_config=fsc,
                timestamp_key="timestamp",
                from_source=False,
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        expected_df = (
            self._get_spark_df(
                ["A", "B", "C", "timestamp", "bound_tfv.score", "wildcard_tfv.score"],
                [
                    [1, 1, "X", "2018-10-30T15:01:00Z", 20, 22],
                    [1, 1, "Y", "2018-10-30T15:01:00Z", 20, 33],
                    [1, 2, "X", "2018-10-30T15:01:00Z", 50, 44],
                    [1, 2, "Y", "2018-10-30T15:01:00Z", 50, 55],
                    [3, 3, "Z", "2018-10-30T15:01:00Z", None, 66],
                    [10, 10, None, "2018-10-30T15:01:00Z", None, None],
                    [1, 1, "X", "2018-10-30T13:01:00Z", 10, 22],
                    [1, 2, None, "2018-10-30T13:01:00Z", 40, None],
                    [3, 3, None, "2018-10-30T13:01:00Z", 60, None],
                ],
                "timestamp",
            )
            .toPandas()
            .sort_index(axis=1)
            .sort_values(by=["A", "B", "C", "timestamp"])
            .reset_index(drop=True)
        )

        pandas.testing.assert_frame_equal(training_dataset, expected_df)

    @patch("tecton._internals.metadata_service._stub_instance")
    def test_online_namespaces_fv(self, metadata_service):
        def my_online_transform(greeting) -> pandas.DataFrame:
            import pandas

            series = [{"greeting_length": len(row["greeting"])} for _, row in greeting.iterrows()]
            return pandas.DataFrame(series)

        feature_package = feature_package_pb2.FeaturePackage()
        feature_view = FeatureView()
        feature_view.fco_metadata.name = "test_fv1"

        feature_view.on_demand_feature_view.CopyFrom(OnDemandFeatureView())

        transformation = self._create_transformation(my_online_transform, TransformationMode.TRANSFORMATION_MODE_PANDAS)
        feature_view.schemas.materialization_schema.CopyFrom(
            Schema.from_spark(StructType([StructField(f"greeting_length", LongType())])).to_proto()
        )

        pipeline = Pipeline()

        request_context = RequestContext(schema={"greeting": StringType()})

        request_data_source_node = RequestDataSourceNode()
        request_data_source_node.request_context.CopyFrom(request_context._to_proto())
        request_data_source_node.input_name = "greeting"

        input_pipeline_node = PipelineNode()
        input_pipeline_node.request_data_source_node.CopyFrom(request_data_source_node)

        transformation_input = Input()
        transformation_input.arg_name = "greeting"
        transformation_input.node.CopyFrom(input_pipeline_node)

        transformation_node = TransformationNode()
        transformation_node.transformation_id.CopyFrom(transformation.transformation_id)
        transformation_node.inputs.append(transformation_input)

        transformation_pipeline_node = PipelineNode()
        transformation_pipeline_node.transformation_node.CopyFrom(transformation_node)
        pipeline.root.CopyFrom(transformation_pipeline_node)

        feature_view.pipeline.CopyFrom(pipeline)

        feature_view.enrichments.transformations.append(transformation)

        fv1 = tecton.interactive.FeatureView(feature_view)
        fpov = FeaturePackageOrView.of(fv1._proto)

        fsc = FeatureSetConfig()
        fsc._add(fpov)
        fsc._add(fpov, namespace="ns1")

        spine_df = self.spark.createDataFrame(pandas.DataFrame([{"greeting": "hello"}, {"greeting": "goodbye"}]))

        expected_df = pandas.DataFrame(
            [
                {"greeting": "hello", "test_fv1.greeting_length": 5, "ns1.greeting_length": 5},
                {"greeting": "goodbye", "test_fv1.greeting_length": 7, "ns1.greeting_length": 7},
            ]
        )

        actual_df = data_frame_helper.get_features_for_spine(
            self.spark, spine_df=spine_df, feature_set_config=fsc, timestamp_key=None, from_source=True
        ).toPandas()

        pandas.testing.assert_frame_equal(actual_df, expected_df)
