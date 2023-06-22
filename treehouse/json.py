from json import JSONEncoder
from uuid import UUID
from pandas import Timestamp


class StamJSONEncoder(JSONEncoder):
    def default(self, z):
        if isinstance(z, Timestamp):
            return z.strftime("%Y-%m-%d %H:%M:%S %Z")
        elif isinstance(z, UUID):
            return str(z)
        elif isinstance(z, (int, float, bool)):
            return str(z)
        else:
            return super().default(z)
