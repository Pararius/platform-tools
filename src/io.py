import csv
from google.cloud.storage import Client as storageClient
import json
from pandas import DataFrame
from io import BytesIO, StringIO
import gcsfs
from pyarrow import parquet


def read_jsons_from_bucket(bucket: str, prefix: str, client: storageClient) -> list:
    """
    read_jsons_from_bucket(bucket:str, prefix:str, client:storageClient = None)

    Reads all JSON files that are found under the provided prefix and returns a list of JSON objects
    """

    json_files = list(client.list_blobs(bucket, prefix=prefix))

    json_list = []

    if len(json_files) > 0:
        for file in json_files:
            json_list.append(json.loads(file.download_as_bytes().decode("UTF-8")))

    return json_list


def read_parquet_from_bucket(bucket: str, prefix: str) -> DataFrame:
    url = f"gs://{bucket}/{prefix}"
    fs = gcsfs.GCSFileSystem()

    print(fs.glob("bla"))
    files = ["gs://" + path for path in fs.glob(url + "/*.parquet")]
    ds = parquet.ParquetDataset(files, filesystem=fs)
    df = ds.read().to_pandas()

    return df


def write_dataframe_to_parquet(
    df: DataFrame,
    bucket: str,
    prefix: str,
    client: storageClient,
) -> bool:
    """
    write_dataframe_to_parquet(df:DataFrame, bucket:str, prefix:str, client:storageClient = storageClient())

    Writes a Pandas dataframe to a parquet blob in GCP storage
    """
    bucket = client.bucket(bucket)

    blob = bucket.blob(prefix)

    buff = BytesIO()

    df.to_parquet(buff, index=False)

    try:
        blob.upload_from_string(buff.getvalue())

        return True
    except:
        return False


def create_csv_reader_from_bucket(
    bucket: str, prefix: str, client: storageClient
) -> csv.DictReader:
    bucket = client.bucket(bucket)
    file = bucket.blob(prefix)
    scsv = file.download_as_bytes().decode("UTF-8")
    f = StringIO(scsv)
    reader = csv.DictReader(f, delimiter=";", quotechar='"')

    return reader


def wrap_payload_for_raw_storage(payload: dict, target_path: str) -> dict:
    return {
        "payload": payload,
        "target_path": target_path,
    }
