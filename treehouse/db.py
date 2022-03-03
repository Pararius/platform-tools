import io
import csv
import pandas as pd
import sqlalchemy
from google.cloud.storage import Client as GCSClient
from sqlalchemy.engine import Engine
from treehouse.storage import set_blob_contents, get_blob


def create_mysql_connection(
    host: str, port: int, username: str, password: str, database: str
) -> Engine:
    return sqlalchemy.create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )


def create_cloudsql_postgres_connection(user: str, password: str, database: str, socket_dir: str, instance_connection_name: str) -> Engine:
    return sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        # Note: Some drivers require the `unix_sock` query parameter to use a different key.
        # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=user,
            password=password,
            database=database,
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    socket_dir, instance_connection_name  # e.g. "/cloudsql"
                )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            },
        ),
    )

def query_to_csv(
    query: str,
    bucket_name: str,
    target_path: str,
    db_connection: Engine,
    storage_client=GCSClient(),
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
