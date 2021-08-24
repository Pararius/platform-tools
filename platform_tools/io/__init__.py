from google.cloud.storage import Client as storageClient
import json

def read_jsons_from_bucket(bucket:str, prefix:str, client:storageClient = None) -> list:
    '''
        read_jsons_from_bucket(bucket:str, prefix:str, client:storageClient = None)

        Reads all JSON files that are found under the provided prefix and returns a list of JSON objects
    '''
    if client is None:
        client = storageClient()


    json_files = list(client.list_blobs(bucket, prefix=prefix))

    json_list = []

    if len(json_files) > 0:
        for file in json_files:
            json_list.append(json.loads(file.download_as_bytes().decode('UTF-8')))

    return json_list
