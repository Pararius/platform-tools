import datetime
import json
import sys
import re
import uuid
from typing import Tuple


def get_parameters(arg_num: int = 1) -> dict:
    # Load arguments from trigger event
    params = json.loads(sys.argv[arg_num])

    return params


def params_from_prefix(
    prefix: str,
    reg_pattern: str = "(?P<name>[a-zA-Z0-9\.\-\_]+)=(?P<value>[a-zA-Z0-9\.\-\_]+)\/",
) -> dict:
    pat = re.compile(reg_pattern)
    params = {}

    for m in pat.finditer(prefix):
        params[m["name"]] = m["value"]

    return params


def param_from_prefix(
    prefix: str, param: str, reg_pattern: str = "([a-zA-Z0-9\.\-\_]+)\/"
) -> str:
    match = re.search(r"\/" + f"{param}={reg_pattern}", prefix)

    if not match or not match.group(1):
        raise Exception(
            f"Failed to extract the value of {param} from the prefix ({prefix})"
        )

    param_value = match.group(1)

    return param_value


# TODO replace with a cleaner solution such as https://pypi.org/project/cron-converter/
def interval_to_timestamp_range(interval: str) -> Tuple[datetime.datetime, datetime.datetime]:
    now = datetime.datetime.today()
    if interval == "every hour":
        previous_hour = now - datetime.timedelta(hours=1)
        current_hour = now

        return previous_hour.replace(minute=0, second=0, microsecond=0), current_hour.replace(minute=0, second=0, microsecond=0)

    raise Exception(f"Unknown interval: {interval}")


def create_extracted_object_id(
    prefix: str,
    data_type: str,
    data_source: str,
    ingestion_timestamp: datetime.datetime
) -> str:
    return \
        f"{prefix.strip('/')}/" if prefix != "" else "" \
        f"/format=json" \
        f"/type={data_type}" \
        f"/source={data_source}" \
        f"/ingestion_date={ingestion_timestamp.strftime('%Y-%m-%d')}" \
        f"/ingestion_hour={ingestion_timestamp.strftime('%H')}" \
        f"/{uuid.uuid4()}.json"


def create_loaded_path(
    bucket_with_prefix: str,
    data_type: str,
    data_source: str,
    ingestion_date: str,
    ingestion_hour: int
) -> str:
    return \
        f"gs://{bucket_with_prefix.strip('/')}" \
        f"/format=parquet" \
        f"/type={data_type}" \
        f"/source={data_source}" \
        f"/ingestion_date={ingestion_date}" \
        f"/ingestion_hour={ingestion_hour}" \
        f"/{uuid.uuid4()}.parquet"
