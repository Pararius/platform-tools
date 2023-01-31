from typing import Union
from pyspark.sql import SparkSession, DataFrame, Column
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    FloatType,
    DateType,
)
from pyspark.sql.functions import lit, col, udf, when
from datetime import datetime, timedelta
import re
import json
import sys
from urllib.parse import urlparse
import base64
from pyspark.sql.utils import AnalysisException


def get_spark_schema(dict_schema):
    """
    get_spark_schema(dict_schema)

    Translates a dictionary of column:datatype pairs into a Spark compatible
    schema

    Currently supports these datatypes:
        - string
        - integer
        - float
        - boolean
        - array[sub_type]

    * for arrays/records it is required to specify the subtype

    Input:
        - dict_schema: dict
            a dictionary of column:datatype pairs

    Returns:
        - spark_schema: StructType
            Spark compatible translation of the input schema
    """

    def __get_dtype(dtype_str):
        if dtype_str in ("str", "string", "object"):
            return StringType()
        elif dtype_str in ("int", "integer", "int32", "int64"):
            return IntegerType()
        elif dtype_str in ("decimal", "float", "float32", "float64"):
            return FloatType()
        elif dtype_str in ("date"):
            return DateType()
        elif dtype_str in ("datetime", "datetime64", "timestamp"):
            return TimestampType()
        elif dtype_str in ("bool", "boolean"):
            return BooleanType()
        elif dtype_str[:6] == "struct":
            return StructType(
                fields=[
                    StructField(name=m[0], dataType=__get_dtype(m[1]))
                    for m in re.findall(r"\<?([a-z0-9]*):([a-z]*)\>?", dtype_str)
                ]
            )
        elif dtype_str[:5] in ("recor", "array"):
            sub_type_str = re.search(r"\[(.*?)]", dtype_str).group(1)

            if sub_type := __get_dtype(sub_type_str):
                return ArrayType(sub_type)
            else:
                return False
        else:
            return False

    spark_schema = []

    for col, type in dict_schema.items():

        if spark_type := __get_dtype(type):
            spark_schema.append(StructField(col, spark_type, True))
        else:
            print(f"Unknown type {type}, ommiting col {col} from schema")

    return StructType(spark_schema)


def enforce_schema(df, schema):
    """
    enforce_schema(df, schema):

    Enforces the specified schema on a dataframe.

    This means:
    - Adding missing columns from schema with the correct datatype,
    - Making sure each column is cast to the correct datatype
    - Dropping columns that are not in the schema

    Input:
        - df: Dataframe
            the Spark Dataframe to act on
        - schema: StructType
            the schema that the Dataframe should adhere to

    Output:
        - df: Dataframe
            the corrected version of the input Dataframe
    """
    return df.select(
        *[
            col(c.name).cast(c.dataType)
            if c.name in df.columns
            else lit(None).cast(c.dataType).alias(c.name)
            for c in schema
        ]
    )


def get_date_list(base_date, window, date_fmt="%Y-%m-%d"):
    """
    get_date_list(base_date, window, date_fmt)

    Returns a list of (2 * window + 1) calendar dates centered on base_date

    Input:
        - base_date: str
            the center date for the list, should be a atring that can be parsed to datetime object using the format in date_fmt
        - window: int
            number of days before and after base_date to include in the list
        - date_fmt: str
            a datetime compatible date format. This determines the format of the input as well as the resulting output

    Output:
        - dates: list
            a list of dates centered around base_date
    """
    base = datetime.strptime(base_date, date_fmt)

    date_list = [base + timedelta(days=x) for x in range(-window, window + 1, 1)]

    return [d.strftime(date_fmt) for d in date_list]


def flatten_df(nested_df, exclude_paths=[], separator="_", max_depth=None):
    """
    flatten_df(nested_df)

    Takes all columns with the Struct datatype from a dataframe and adds the fields as individual
    columns to the original dataframe, using the original column as a prefix

    Input:
        - nested_df: Dataframe
        - max_depth: control the level to flatten (optional)

    Returns:
        - flat_df: Dataframe
    """

    exclude_paths = [p.replace(".", "_") for p in exclude_paths]

    flat_cols = [c[0] for c in nested_df.dtypes if c[1][:6] != "struct"]
    nested_cols = [
        c[0]
        for c in nested_df.dtypes
        if (c[1][:6] == "struct") & (c[0] not in exclude_paths)
    ]
    nested_but_excluded_cols = [
        c[0]
        for c in nested_df.dtypes
        if (c[1][:6] == "struct") & (c[0] in exclude_paths)
    ]

    # No structs left to flatten, return result
    if len(nested_cols) == 0:
        return nested_df

    flat_df = nested_df.select(
        flat_cols
        + nested_but_excluded_cols
        + [
            col(nc + "." + c).alias(nc + separator + c)
            for nc in nested_cols
            for c in nested_df.select(nc + ".*").columns
        ]
    )

    if max_depth is not None:
        if max_depth > 1:
            return flatten_df(flat_df, exclude_paths, max_depth - 1)
        else:
            return flat_df
    else:
        return flatten_df(flat_df, exclude_paths)


def create_spark_session(app_name: str, enable_bigquery: bool = True) -> SparkSession:
    spark = (
        SparkSession.builder.appName(app_name)
        .config(
            "spark.sql.parquet.int96RebaseModeInRead", "LEGACY"
        )  # Backwards comp. for older Spark versions
        .config("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY")
        # .config(
        #     "spark.sql.legacy.parquet.int96RebaseModeInRead", "CORRECTED"
        # )  # Backwards comp. for older Spark versions
        .config(
            "spark.sql.parquet.int96RebaseModeInWrite", "LEGACY"
        )  # Backwards comp. for older Spark versions
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
        # .config(
        #     "spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED"
        # )  # Backwards comp. for older Spark versions
        .config(
            "mapreduce.fileoutputcommitter.marksuccessfuljobs", "false"
        )  # Don't write _SUCCESS files
        .config(
            "spark.sql.sources.partitionOverwriteMode", "dynamic"
        )  # Only UPSERT when overwriting partioned data
        .config("spark.sql.parquet.mergeSchema", "false")
        .config("spark.sql.parquet.filterPushdown", "true")
        .config("spark.reducer.maxReqsInFlight", "1")
        .config("spark.shuffle.io.retryWait", "60s")
        .config("spark.shuffle.io.maxRetries", "10")
        .config("mapreduce.fileoutputcommitter.algorithm.version", "2")
        .getOrCreate()
    )

    # BigQuery-specific settings
    if enable_bigquery:
        spark.conf.set("viewsEnabled", "true")
        spark.conf.set("materializationDataset", "spark_staging")

    return spark


def write_dataframe_to_bucket(
    df: DataFrame,
    destination: str,
    partition_by: list = [],
    num_partitions: int = None,
    mode: str = "overwrite",
    format: str = "parquet",
) -> bool:
    # Write joined dataset
    try:
        if num_partitions is not None:
            df = df.repartition(num_partitions)

        if len(partition_by) >= 1:
            df.write.partitionBy(*partition_by).mode(mode).format(format).save(
                destination
            )
        else:
            df.write.mode(mode).format(format).save(destination)
        return True
    except Exception as e:
        raise (e)


def get_parameters(arg_num: int = 1) -> dict:
    # Load arguments from trigger event
    params = json.loads(base64.b64decode(sys.argv[arg_num]).decode())

    return params


@udf(returnType=StringType())
def parse_furnished_type(furnished_list):
    result = []

    if furnished_list is None:
        return "unknown"

    # Convert to list
    if isinstance(furnished_list, str):
        furnished_list = [furnished_list]

    # Cast to lowercase for comparison
    furnished_list = [i.lower() for i in furnished_list]

    if ("furnished" in furnished_list) or ("gemeubileerd" in furnished_list):
        result.append("furnished")

    if ("shell" in furnished_list) or ("kaal" in furnished_list):
        result.append("shell")

    if ("upholstered" in furnished_list) or ("gestoffeerd" in furnished_list):
        result.append("upholstered")

    if len(result) > 0:
        return " or ".join(result)
    else:
        return "unknown"


@udf(returnType=ArrayType(StringType()))
def parse_facilities(facility_list):
    return [f for f in facility_list if (f is not None) and (f != "")]


@udf(returnType=StringType())
def extract_hostname(uri: str) -> str:
    return urlparse(uri).hostname


@udf(returnType=StringType())
def extract_path(uri: str) -> str:
    return urlparse(uri).path


@udf(returnType=StringType())
def extract_query_string(uri: str) -> str:
    return urlparse(uri).query


@udf(returnType=StringType())
def extract_fragment(uri: str) -> str:
    return urlparse(uri).fragment


def map_strict(
    df: DataFrame, source_col: Union[str, Column], target_col: str, mapping: dict
) -> DataFrame:

    if isinstance(source_col, str):
        source_col = df[source_col]

    return df.withColumn(
        target_col,
        when(source_col.isin(list(mapping.keys())), source_col),
    ).replace(mapping, subset=target_col)


def safe_col(df: DataFrame, path: str) -> Column:
    try:
        var = df[path]
        return col(path)
    except AnalysisException:
        return lit(None)
