import csv
from typing import Callable
from concurrent import futures
from google.cloud.storage import Client as storageClient
from google.cloud import pubsub_v1
import json
from pandas import DataFrame
from io import BytesIO, StringIO
import gcsfs
from pyarrow import parquet


def read_jsons_from_bucket(
    bucket: str, prefix: str, client: storageClient = storageClient()
) -> list:
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


def read_parquet_from_bucket(
    bucket: str, prefix: str, client: storageClient = storageClient()
) -> DataFrame:
    url = f"gs://{bucket}/{prefix}"
    fs = gcsfs.GCSFileSystem()

    files = ["gs://" + path for path in fs.glob(url + "/*.parquet")]
    ds = parquet.ParquetDataset(files, filesystem=fs)
    df = ds.read().to_pandas()

    return df


def write_dataframe_to_parquet(
    df: DataFrame,
    bucket: str,
    prefix: str,
    client: storageClient = storageClient(),
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
    bucket: str, prefix: str, client: storageClient = storageClient()
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


def gen_chunks(reader, chunksize=100):
    chunk = []
    for i, line in enumerate(reader):
        if i % chunksize == 0 and i > 0:
            yield chunk
            chunk = []
        chunk.append(line)
    yield chunk


def get_pubsub_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            publish_future.result(timeout=60)
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


# see https://cloud.google.com/pubsub/docs/publisher#publishing_messages
def publish_messages(
    iterator,
    project: str,
    topic: str,
    chunk_size: int = 500,
    transform_callback = None,
    publisher: pubsub_v1.PublisherClient = pubsub_v1.PublisherClient(),
) -> bool:
    topic_path = publisher.topic_path(project, topic)
    lines_done = 0

    for chunk in gen_chunks(iterator, chunksize=chunk_size):
        publish_futures = []

        for data in chunk:
            if callable(transform_callback):
                data = transform_callback(data)

            content = json.dumps(data)

            # # When you publish a message, the client returns a future.
            publish_future = publisher.publish(topic_path, content.encode("UTF-8"))

            # # Non-blocking. Publish failures are handled in the callback function.
            publish_future.add_done_callback(get_pubsub_callback(publish_future, content))
            publish_futures.append(publish_future)

        # Wait for all the publish futures to resolve before continuing.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        # Keep track of progress for debugging
        lines_done += len(chunk)
        print(f"Published {lines_done} records sofar")

    return True
