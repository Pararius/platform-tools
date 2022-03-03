import io
import csv
import pandas as pd
from google.cloud.storage import Client as GCSClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from treehouse.storage import set_blob_contents, get_blob


def create_mysql_connection(
    host: str, port: int, username: str, password: str, database: str
) -> Engine:
    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )


def query_to_csv(
    query: str,
    bucket_name: str,
    target_path: str,
    db_connection: Engine,
    storage_client: GCSClient,
):
    df = pd.read_sql(
        query,
        con=db_connection,
    )

    buff = io.StringIO()
    df.to_csv(path_or_buf=buff, sep=";", quoting=csv.QUOTE_ALL)

    blob = get_blob(
        bucket_name,
        target_path,
        storage_client,
    )

    set_blob_contents(blob, buff.getvalue(), "text/csv")
