from typing import Dict, Callable

import pandas
from orjson import loads


def excel_to_json(path: str, sheet_name: str, id_col_name: str = "ID",
                  drop_predicate: Callable[[Dict], bool] = lambda _: False, **kwargs):
    payload = loads(pandas.read_excel(path, sheet_name=sheet_name, **kwargs).to_json())
    ids = payload.pop(id_col_name)
    headers = list(payload.keys())
    return list(val for val in (
        {
            header: payload.get(header).get(i)
            for header in headers
        } for i in ids
    ) if not drop_predicate(val))
