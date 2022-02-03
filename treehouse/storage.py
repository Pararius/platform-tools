import csv
from typing import Callable
from google.cloud.exceptions import GoogleCloudError, NotFound
from google.cloud.storage import Client, Blob
import json
from pandas.core.frame import DataFrame
from pandas import read_parquet
import os
from io import BytesIO
from uuid import uuid4


def get_blob(bucket: str, prefix: str, client: Client) -> Blob:
    bucket = client.bucket(bucket)

    return bucket.blob(prefix)


def set_blob_contents(
    blob: Blob, content: str, content_type: str = "text/plain"
) -> bool:
    """
    Uploads content for a given blob and suppresses any exceptions that may be thrown
    """

    try:
        blob.upload_from_string(content, content_type=content_type)

        return True
    except GoogleCloudError as exception:
        print(f"Failed to set contents of the given blob: {exception}")

        return False


def get_blob_contents(blob: Blob) -> str:
    """
    Returns the contents of a blob as a UTF-8 decoded string
    """

    try:
        return blob.download_as_bytes().decode("UTF-8")
    except NotFound as exception:
        print(f"Failed to retrieve contents of the given blob: {exception}")

        raise exception


def get_object_generation(bucket: str, prefix: str, client: Client) -> int:
    """
    Returns the generationId of a blob as an integer
    """
    bucket = client.get_bucket(bucket)

    blob = bucket.get_blob(prefix)

    return blob.generation


def download_blob_contents(
    bucket: str, prefix: str, local_file_name: str, client: Client
) -> bool:
    """
    Downloads the contents of a blob from the bucket to a local file
    """

    blob = get_blob(bucket, prefix, client)
    try:
        blob.download_to_filename(local_file_name)

        return True
    except:
        return False


def read_jsons_from_bucket(bucket: str, prefix: str, client: Client) -> list:
    """
    Reads all JSON files that are found under the provided prefix and returns a list of JSON objects
    """

    json_files = list(client.list_blobs(bucket, prefix=prefix))

    json_list = []

    if len(json_files) > 0:
        for file in json_files:
            json_list.append(json.loads(get_blob_contents(file)))

    return json_list


def read_parquet_from_bucket(bucket: str, prefix: str, client: Client) -> DataFrame:
    """
    Read a single parquet file from a given bucket's prefix and return as a Pandas DataFrame
    """

    df = DataFrame([])

    # Download data to local storage
    tmp_file_name = f"/tmp/data-{str(uuid4())}.parquet"
    if download_blob_contents(bucket, prefix, tmp_file_name, client):

        df = read_parquet(tmp_file_name)

        # Clean up to prevent OOM
        if os.path.exists(tmp_file_name):
            os.remove(tmp_file_name)

    return df


def write_dataframe_to_parquet(
    dataframe: DataFrame, bucket: str, prefix: str, client: Client
) -> bool:
    """
    Writes a Pandas dataframe to a parquet blob in GCP storage
    """

    try:
        blob = get_blob(bucket, prefix, client)
        buff = BytesIO()

        dataframe.to_parquet(buff, index=False)

        set_blob_contents(blob, buff.getvalue())

        return True
    except Exception as e:
        print(e)
        return False


def write_dataframe_to_partitioned_parquet(
    dataframe: DataFrame,
    partition_col: str,
    bucket: str,
    prefix: str,
    client: Client,
) -> bool:

    # temporary function to write partitioned files until bug in gcsfs is fixed
    # issue: https://issuetracker.google.com/issues/202804016
    # note: this only supports a single partition column (to avoid recursion hell)

    for col_val in dataframe[partition_col].unique():

        _prefix = prefix + f"{partition_col}={col_val}/{str(uuid4())}.parquet"

        blob = get_blob(bucket, _prefix, client)
        buff = BytesIO()

        dataframe[dataframe[partition_col] == col_val].reset_index(
            drop=True
        ).to_parquet(buff, index=False)

        set_blob_contents(blob, buff.getvalue())

    return True


def process_csv_in_blocks(
    path: str,
    processor: Callable,
    separator: str = ";",
    block_size: str = "10MB",
) -> csv.reader:
    """
    Reads a CSV file in blocks to reduce memory consumption.
    Every block is then passed to the given `processor` as a DataFrame.

    Source: https://medium.com/analytics-vidhya/optimized-ways-to-read-large-csvs-in-python-ab2b36a7914e

    path -- the path to the CSV file (can be a local path or any value that can be handled by Dask such as GCS object IDs)
    processor -- the callable that is used on every block
    separator -- the separator used in the targeted CSV
    block_size -- the maximum size of the blocks passed to the processor
    """
    import dask.dataframe as dd

    df = dd.read_csv(path, blocksize=block_size, sep=separator, dtype=str)
    df.map_partitions(processor).compute()


def wrap_payload_for_raw_storage(payload: dict, target_path: str) -> dict:
    return {
        "payload": payload,
        "target_path": target_path,
    }


def is_object(bucket: str, prefix: str, client: Client) -> bool:
    """Validates whether the specified prefix points to an existing object

    Args:
        bucket (str): bucket
        prefix (str): object prefix
        client (Client): google-cloud-storage Client

    Returns:
        bool: [description]
    """
    blob = get_blob(bucket, prefix, client)

    try:
        # Get blob info from bucket
        blob.reload()
    except:
        # If we fail to get info, it's not a valid object
        return False

    # Folders have size 0, proper objects don't
    return blob.size > 0


def is_folder(bucket: str, prefix: str, client: Client) -> bool:
    """Validates whether the specified prefix points to a folder (as opposed to an object)

    Args:
        bucket (str): bucket
        prefix (str): folder prefix
        client (Client): google-cloud-storage Client

    Returns:
        bool: [description]
    """
    blob = get_blob(bucket, prefix, client)

    try:
        # Get blob info from bucket
        blob.reload()
    except:
        # If we fail to get info, it's not a valid object
        return False

    # Folders have size 0, proper objects don't
    return blob.size == 0
