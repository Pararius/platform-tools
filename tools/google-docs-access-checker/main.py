# https://reclabs.atlassian.net/browse/DATA-884
from typing import Tuple
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# - scan for docs
# - for each doc:
#     - check sharing scope: if public, log it
# - (optional) send message to slack (#stam-alerts)


def scan_docs():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    try:
        service = build("drive", "v3")

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            return []

        public = []
        print("Files:")
        for item in items:
            print(item)
            print(f"{item['name']} ({item['id']})")
            public.append(item['name'])

        return public
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


def filter_public_docs(docs: list) -> []:
    return []


def handler(request=None) -> Tuple[str, int]:
    # data = request.get_json(silent=True) or {}
    docs = scan_docs()

    if len(docs) == 0:
        return (
            f"No documents found, perhaps the configured service account does not have enough permission to view them?",
            200,
        )

    public_docs = filter_public_docs(docs)

    if len(public_docs) > 0:
        # report to Slack?
        return (
            f"Detected {len(public_docs)} public docs, they have been reported in #stam-alerts",
            200,
        )

    return "No public docs detected", 200
