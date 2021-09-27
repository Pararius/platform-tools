import csv

from google.cloud.exceptions import GoogleCloudError, NotFound
from google.cloud.storage import Client, Blob
from datetime import datetime as dt
import json
from pandas import DataFrame
from io import BytesIO, StringIO
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


def read_parquet_from_bucket(bucket: str, prefix: str) -> DataFrame:
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
    df: DataFrame,
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


def create_csv_reader_from_bucket(
    bucket: str, prefix: str, client: Client
) -> csv.DictReader:
    file = get_blob(bucket, prefix, client)
    scsv = get_blob_contents(file)
    f = StringIO(scsv)
    reader = csv.DictReader(f, delimiter=";", quotechar='"')

    return reader


def wrap_payload_for_raw_storage(payload: dict, source: str, type: str, owner: str, target_path: str) -> dict:
    return {
        "payload": payload,
        "metadata": {
            "ingestion_timestamp": dt.now(),
            "source": source,
            "type": type,
            "owner": owner,
        },
        "target_path": target_path,
    }
