import json
from datetime import datetime


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def to_datetime(date_str: str) -> datetime:
    d = date_str
    try:
        dte = datetime.strptime(d, "%Y-%m")
    except ValueError:
        dte = date_str
    return dte


class JsonCleaner(object):
    def __init__(self, transformed=None):
        self.trans = transformed

    def clean_json(self, json_dict: dict):
        clean_dict = dict()
        for k, v in json_dict.items():
            if type(v) is dict:
                # values are columns
                if v.values():
                    values = list(v.values())[0]
                    clean_dict.update(self._clean_looker_columns(values))
            else:
                # value is primary key
                clean_dict[self._transform_looker_key(k)] = to_datetime(v)
        return clean_dict

    def _transform_looker_key(self, key: str):
        """
        Removes caps and periods from key
        (seen in some json responses frm looker)
        """
        return key if self.trans is None else self.trans.get(key, key)

    def _clean_looker_columns(self, columns_dict):
        clean_dict = dict()
        for key, value in columns_dict.items():
            clean_dict[self._transform_looker_key(key)] = value
        return clean_dict

