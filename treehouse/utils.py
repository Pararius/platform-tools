import json
import sys
import re


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
