from typing import Callable
from concurrent import futures
from google.cloud import pubsub_v1
import json
from .optimization import split_into_chunks


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


def publish_messages(
    publisher: pubsub_v1.PublisherClient,
    iterator,
    project: str,
    topic: str,
    chunk_size: int = 500,
    transform_callback=None,
) -> bool:
    topic_path = publisher.topic_path(project, topic)
    lines_done = 0

    for chunk in split_into_chunks(iterator, chunksize=chunk_size):
        publish_futures = []

        for data in chunk:
            if callable(transform_callback):
                data = transform_callback(data)

            content = json.dumps(data)

            # # When you publish a message, the client returns a future.
            publish_future = publisher.publish(topic_path, content.encode("UTF-8"))

            # # Non-blocking. Publish failures are handled in the callback function.
            publish_future.add_done_callback(
                get_pubsub_callback(publish_future, content)
            )
            publish_futures.append(publish_future)

        # Wait for all the publish futures to resolve before continuing.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        # Keep track of progress for debugging
        lines_done += len(chunk)
        print(f"Published {lines_done} records sofar")

    return True
