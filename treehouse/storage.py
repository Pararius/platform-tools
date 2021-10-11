import csv
from typing import Callable
from google.cloud.exceptions import GoogleCloudError, NotFound
from google.cloud.storage import Client, Blob
import json
from io import BytesIO
import gcsfs
from pyarrow import parquet


def set_blob_contents(blob: Blob, content) -> bool:
    """
    Uploads content for a given blob and suppresses any exceptions that may be thrown
    """

    try:
        blob.upload_from_string(content)

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


def read_parquet_from_bucket(bucket: str, prefix: str) -> object:
    """
    Read a single parquet file from a given bucket's prefix and return as a Pandas DataFrame
    """

    url = f"gs://{bucket}/{prefix}"
    fs = gcsfs.GCSFileSystem()
    ds = parquet.ParquetDataset(url, filesystem=fs)
    df = ds.read().to_pandas()

    return df


def read_multi_parquet_from_bucket(bucket: str, prefix: str) -> object:
    """
    Reads all parquet files from a given bucket's prefix and returns them as a single Pandas DataFrame
    """

    url = f"gs://{bucket}/{prefix}"
    fs = gcsfs.GCSFileSystem()
    files = ["gs://" + path for path in fs.glob(url + "/*.parquet")]
    ds = parquet.ParquetDataset(files, filesystem=fs)
    df = ds.read().to_pandas()

    return df


def get_blob(bucket: str, prefix: str, client: Client) -> Blob:
    bucket = client.bucket(bucket)

    return bucket.blob(prefix)


def write_dataframe_to_parquet(
    df,
    bucket: str,
    prefix: str,
    client: Client,
) -> bool:
    """
    Writes a Pandas dataframe to a parquet blob in GCP storage
    """
    blob = get_blob(bucket, prefix, client)
    buff = BytesIO()

    df.to_parquet(buff, index=False)

    return set_blob_contents(blob, buff.getvalue())


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
