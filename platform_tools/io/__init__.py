from google.cloud.storage import Client as storageClient
import json
import pandas
from io import BytesIO

def read_jsons_from_bucket(bucket:str, prefix:str, client:storageClient = storageClient()) -> list:
    '''
        read_jsons_from_bucket(bucket:str, prefix:str, client:storageClient = None)

        Reads all JSON files that are found under the provided prefix and returns a list of JSON objects
    '''

    json_files = list(client.list_blobs(bucket, prefix=prefix))

    json_list = []

    if len(json_files) > 0:
        for file in json_files:
            json_list.append(json.loads(file.download_as_bytes().decode('UTF-8')))

    return json_list

def write_dataframe_to_parquet(df:pandas.DataFrame, bucket:str, prefix:str, client:storageClient = storageClient()) -> bool:
    '''
        write_dataframe_to_parquet(df:pandas.DataFrame, bucket:str, prefix:str, client:storageClient = storageClient())

        Writes a Pandas dataframe to a parquet blob in GCP storage
    '''    
    bucket = client.bucket(bucket)

    blob = bucket.blob(prefix)

    buff = BytesIO()

    df.to_parquet(buff, index=False)

    try:
        blob.upload_from_string(buff.getvalue())

        return True
    except:
        return False