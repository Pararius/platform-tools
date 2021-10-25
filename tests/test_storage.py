import json
from csv import DictReader
from os import write

from gcsfs import GCSFileSystem
from google.cloud.exceptions import GoogleCloudError
from pyarrow import parquet

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

@patch("google.cloud.storage")
def test_read_parquet_from_bucket(mock_storage, monkeypatch):
    from pandas import DataFrame

    bucket = "my-bucket"
    prefix = "my-prefix"

    monkeypatch.setattr("treehouse.storage.download_blob_contents", MagicMock(return_value=True))
    monkeypatch.setattr("treehouse.storage.read_parquet", Mock(return_value=DataFrame([])))

    mock_gcs_client = mock_storage.Client.return_value

    # for some reason this needs to use the 'with' construction instead of '@patch' annotation like other tests
    df = io.read_parquet_from_bucket(bucket, prefix, mock_gcs_client)

    assert type(df) == DataFrame


@patch("gcsfs.GCSFileSystem", autospec=True)
def test_write_dataframe_to_parquet_success(mock_fs):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"

    with patch.object(parquet, "write_table", autospec=True):
        result = io.write_dataframe_to_parquet(
            df=df, bucket=bucket, prefix=prefix, fs=mock_fs
        )

        assert result == True


@patch("gcsfs.GCSFileSystem", autospec=True)
def test_write_dataframe_to_parquet_failure(mock_fs):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"

    write_table = Mock()
    write_table.side_effect = Exception("Not good!")

    with patch.object(parquet, "write_table", write_table):
        result = io.write_dataframe_to_parquet(
            df=df, bucket=bucket, prefix=prefix, fs=mock_fs
        )

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
