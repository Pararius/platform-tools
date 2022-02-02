import json
import sys


def get_parameters(argNum: int = 1) -> dict:
    # Load arguments from trigger event
    params = json.loads(sys.argv[argNum])

    return params
