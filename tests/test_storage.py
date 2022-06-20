import json

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

    monkeypatch.setattr(
        "treehouse.storage.read_parquet", Mock(return_value=DataFrame([]))
    )

    mock_blob = Mock()
    mock_blob.download_to_filename.return_value = True

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    mock_gcs_client = mock_storage.Client.return_value
    mock_gcs_client.bucket.return_value = mock_bucket

    # for some reason this needs to use the 'with' construction instead of '@patch' annotation like other tests
    df = io.read_parquet_from_bucket(bucket, prefix, client=mock_gcs_client)

    assert type(df) == DataFrame


def test_write_dataframe_to_parquet_success(monkeypatch):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"

    blob = Mock()
    client = MagicMock()

    monkeypatch.setattr("treehouse.storage.get_blob", Mock(return_value=blob))
    monkeypatch.setattr("treehouse.storage.set_blob_contents", Mock(return_value=True))

    result = io.write_dataframe_to_parquet(
        dataframe=df, bucket=bucket, prefix=prefix, client=client
    )

    assert result == True


def test_write_dataframe_to_parquet_failure(monkeypatch):
    from pandas import DataFrame

    df = DataFrame()
    bucket = "my-bucket"
    prefix = "my-prefix"

    blob = Mock()
    client = MagicMock()

    monkeypatch.setattr("treehouse.storage.get_blob", Mock(return_value=blob))
    monkeypatch.setattr(
        "treehouse.storage.set_blob_contents", Mock(side_effect=Exception("error!"))
    )

    result = io.write_dataframe_to_parquet(
        dataframe=df, bucket=bucket, prefix=prefix, client=client
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
