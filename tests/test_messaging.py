import json
from concurrent import futures
from unittest.mock import Mock, patch, MagicMock
from src import messaging


def test_get_pubsub_callback():
    future = Mock()
    data = "my-data"
    callback = messaging.get_pubsub_callback(future, data)

    assert callable(callback) == True


@patch("google.cloud.pubsub_v1.PublisherClient")
def test_publish_messages(mock_publisher_client):
    iterator = range(5)
    project = "my-project"
    topic = "my-topic"
    chunk_size = 2

    # for some reason this needs to use the 'with' construction instead of '@patch' annotation like other tests
    with patch.object(futures, "wait", return_value=[]):
        mock_topic_path = Mock()
        mock_publisher_client.topic_path.return_value = mock_topic_path
        result = messaging.publish_messages(
            mock_publisher_client,
            iterator,
            project,
            topic,
            chunk_size,
            transform_callback,
        )

        for value in iterator:
            mock_publisher_client.publish.assert_any_call(
                mock_topic_path, json.dumps(value).encode("UTF-8")
            )

        assert mock_publisher_client.publish.call_count == len(iterator)
        assert result == True


def transform_callback(val):
    return val
