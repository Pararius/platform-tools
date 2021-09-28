import json
from csv import DictReader

from gcsfs import GCSFileSystem
from google.cloud.exceptions import GoogleCloudError

import treehouse.storage as io
from unittest.mock import Mock, patch, MagicMock


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


@patch("pyarrow.parquet.ParquetDataset")
def test_read_parquet_from_bucket(mock_parquet_dataset):
    from pandas import DataFrame

    bucket = "my-bucket"
    prefix = "my-prefix"

    mock_read = Mock()
    mock_read.to_pandas.return_value = DataFrame()
    mock_ds = Mock()
    mock_ds.read.return_value = mock_read
    mock_parquet_dataset.return_value = mock_ds

    # for some reason this needs to use the 'with' construction instead of '@patch' annotation like other tests
    with patch.object(GCSFileSystem, "glob", return_value=[]):
        df = io.read_parquet_from_bucket(bucket, prefix)

        assert type(df) == DataFrame


@patch("google.cloud.storage")
def test_write_dataframe_to_parquet_success(mock_storage):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"

    result = io.write_dataframe_to_parquet(df, bucket, prefix, mock_storage)

    assert result == True


@patch("google.cloud.storage.Client")
def test_write_dataframe_to_parquet_failure(mock_storage_client):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"
    mock_bucket = Mock()
    mock_blob = Mock()
    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.upload_from_string.side_effect = GoogleCloudError("Something went wrong")

    result = io.write_dataframe_to_parquet(df, bucket, prefix, mock_storage_client)

    assert result == False


@patch("google.cloud.storage")
def test_process_csv_in_blocks(mock_storage):
    import pandas as pd

    path = "tests/fixture.csv"
    mock_processor = Mock()
    io.process_csv_in_blocks(path, mock_processor)

    pd.testing.assert_frame_equal(
        mock_processor.call_args[0][0],
        pd.DataFrame(
            data=[
                {"col1": "value1", "col2": "value2"},
                {"col1": "value3", "col2": "value4"},
            ]
        ),
    )

    assert mock_processor.call_count == 2


def test_wrap_payload_for_raw_storage():
    payload = {"foo": "bar"}
    target_path = "path/to/file"

    wrapped_payload = io.wrap_payload_for_raw_storage(payload, target_path)

    assert wrapped_payload["payload"] == payload
    assert wrapped_payload["target_path"] == target_path
