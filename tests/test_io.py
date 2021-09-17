import json
from csv import DictReader

import pandas
from pandas import DataFrame

import src.io as io
from unittest.mock import Mock, patch


@patch("google.cloud.storage")
def test_create_csv_reader_from_bucket(mock_storage):
    bucket = "my-bucket"
    prefix = "my-prefix"
    csv_content = "my;csv"

    mock_bucket = Mock()
    mock_blob = Mock()
    mock_gcs_client = mock_storage.Client.return_value
    mock_gcs_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_bytes.return_value = csv_content.encode("UTF8")

    reader = io.create_csv_reader_from_bucket(bucket, prefix, mock_gcs_client)

    mock_gcs_client.bucket.assert_called_with(bucket)
    mock_bucket.blob.assert_called_with(prefix)
    mock_blob.download_as_bytes.assert_called_once()

    assert type(reader) == DictReader


@patch("google.cloud.storage")
def test_read_jsons_from_bucket(mock_storage):
    bucket = "my-bucket"
    prefix = "my-prefix"
    file_content = '{"foo": "bar"}'
    mock_blobs = []
    expected_result = []

    for x in range(5):
        mock_blob = Mock()
        mock_blob.download_as_bytes.return_value = file_content.encode("UTF8")

        mock_blobs.append(mock_blob)
        expected_result.append(json.loads(file_content))

    mock_gcs_client = mock_storage.Client.return_value
    mock_gcs_client.list_blobs.return_value = mock_blobs

    jsons = io.read_jsons_from_bucket(bucket, prefix, mock_gcs_client)

    mock_gcs_client.list_blobs.assert_called_with(bucket, prefix=prefix)

    assert jsons == expected_result


@patch("gcsfs.GCSFileSystem")
@patch("pyarrow.parquet")
def test_read_parquet_from_bucket(mock_filesystem, mock_parquet):
    bucket = "my-bucket"
    prefix = "my-prefix"

    mock_read = Mock()
    mock_read.to_pandas.return_value = pandas.DataFrame()
    mock_ds = Mock()
    mock_ds.read.return_value = mock_read
    mock_filesystem.glob.return_value = []
    mock_parquet.ParquetDataset.return_value = mock_ds

    df = io.read_parquet_from_bucket(bucket, prefix)

    assert type(df) == DataFrame
