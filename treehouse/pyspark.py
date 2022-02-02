from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    DateType,
    FloatType,
)
from pyspark.sql.functions import lit, col
import re


def create_spark_session(
    app_name: str, master: str = "yarn", enable_bigquery: bool = False
) -> SparkSession:

    spark = (
        SparkSession.builder.appName(appName)
        .master(master)
        .config(
            "spark.sql.parquet.int96RebaseModeInWrite", "LEGACY"
        )  # Backwards comp. for older Spark versions
        .config(
            "spark.sql.legacy.parquet.int96RebaseModeInWrite", "LEGACY"
        )  # Backwards comp. for older Spark versions
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
    mode: str = "overwrite",
    format: str = "parquet",
) -> bool:

    # Write joined dataset
    try:
        if len(partition_by) >= 1:
            df.write.partitionBy(*partition_by).mode(mode).format(format).save(
                destination
            )
        else:
            df.write.mode(mode).format(format).save(destination)
        return True
    except:
        return False


def get_spark_schema(dict_schema: dict) -> StructType:
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
        elif dtype_str in "date":
            return DateType()
        elif dtype_str in ("datetime", "datetime64", "timestamp"):
            return TimestampType()
        elif dtype_str in ("bool", "boolean"):
            return BooleanType()
        elif dtype_str[:5] in ("recor", "array"):
            sub_type_str = re.search(r"\[([\[\]a-zA-Z0-9]*){0,1}\]", dtype_str).group(1)
            if sub_type := __get_dtype(sub_type_str):
                return ArrayType(sub_type)
            else:
                return False
        else:
            return False

    spark_schema = []

    for _col, type in dict_schema.items():

        if spark_type := __get_dtype(type):
            spark_schema.append(StructField(_col, spark_type, True))
        else:
            print(f"Unknown type {type}, ommiting _col {_col} from schema")

    return StructType(spark_schema)


def enforce_schema(df: DataFrame, schema: StructType) -> DataFrame:
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


def flatten_df(nested_df: DataFrame) -> DataFrame:
    """
    flatten_df(nested_df)

    Takes all columns with the Struct datatype from a dataframe and adds the fields as individual
    columns to the original dataframe, using the original column as a prefix

    Input:
        - nested_df: Dataframe

    Returns:
        - flat_df: Dataframe
    """
    flat_cols = [c[0] for c in nested_df.dtypes if c[1][:6] != "struct"]
    nested_cols = [c[0] for c in nested_df.dtypes if c[1][:6] == "struct"]

    flat_df = nested_df.select(
        flat_cols
        + [
            col(nc + "." + c).alias(nc + "_" + c)
            for nc in nested_cols
            for c in nested_df.select(nc + ".*").columns
        ]
    )
    return flat_df
