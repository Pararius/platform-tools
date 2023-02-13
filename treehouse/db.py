import io
import csv
import pandas as pd
import sqlalchemy
from google.cloud.storage import Client as GCSClient
from treehouse.storage import set_blob_contents, get_blob


def create_mysql_connection(
    host: str, port: int, username: str, password: str, database: str
) -> sqlalchemy.engine.Engine:
    return sqlalchemy.create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )


def create_cloudsql_postgres_connection(
    instance_connection_name: str,
    user: str,
    password: str,
    database: str,
    socket_dir="/cloudsql",
) -> sqlalchemy.engine.Engine:
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
                "unix_sock": f"{socket_dir}/{instance_connection_name}/.s.PGSQL.5432"
            },
        ),
    )


def create_cloudsql_mysql_connection(
    instance_connection_name: str,
    user: str,
    password: str,
    database: str,
    socket_dir="/cloudsql",
) -> sqlalchemy.engine.Engine:
    return sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+mysqldb",
            username=user,
            password=password,
            database=database,
            query={"unix_socket": f"{socket_dir}/{instance_connection_name}"},
        ),
    )


def query_to_df(
    query: str,
    db_connection: sqlalchemy.engine.Engine,
) -> pd.DataFrame:
    return pd.read_sql_query(
        sql=sqlalchemy.text(query),
        con=db_connection.connect(),
    )


def query_to_csv(
    query: str,
    bucket_name: str,
    target_path: str,
    db_connection: sqlalchemy.engine.Engine,
    storage_client=GCSClient(),
    skip_when_empty: bool = False,
) -> int:
    df = query_to_df(query, db_connection)

    if skip_when_empty is True & df.shape[0] == 0:
        return 0

    buff = io.StringIO()
    df.to_csv(path_or_buf=buff, sep=";", quoting=csv.QUOTE_ALL)

    blob = get_blob(
        bucket_name,
        target_path,
        storage_client,
    )

    set_blob_contents(blob, buff.getvalue(), "text/csv")

    return df.shape[0]


def query_to_parquet(
    query: str,
    bucket_name: str,
    target_path: str,
    db_connection: sqlalchemy.engine.Engine,
    skip_when_empty: bool = False,
) -> int:
    df = query_to_df(query, db_connection)

    if skip_when_empty is True & df.shape[0] == 0:
        return 0

    # Convert all columns to string
    df[[_col for _col in df.columns]] = df[[_col for _col in df.columns]].astype(
        "string"
    )

    df.to_parquet(f"gs://{bucket_name}/{target_path}")

    return df.shape[0]
