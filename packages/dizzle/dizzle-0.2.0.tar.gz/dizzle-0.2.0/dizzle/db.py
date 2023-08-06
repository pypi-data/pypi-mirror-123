from typing import Dict, Any, List

from sqlalchemy import Table, Column, Integer, String, MetaData, Float

_m = MetaData()


def table_from_dict(name: str, l: List[Dict], *ignore: str,
                    _metadata: MetaData = _m,
                    **size_constraints: Dict[Any, int]):
    if not l:
        raise ValueError("empty list!")
    d = l.pop(0)
    if not size_constraints:
        size_constraints = {}

    def get_type(field: Any):
        if isinstance(field, str):
            return String
        if isinstance(field, int):
            return Integer
        if isinstance(field, float):
            return Float

        raise TypeError(f"{type(field)} is not supported")

    def get_type_constraints(field_value: Any, field_name: str):
        if isinstance(field_value, str):
            return {"length": size_constraints.get(field_name, 255)}
        if isinstance(field_value, int):
            return {}
        if isinstance(field_value, float):
            return {}

        raise TypeError(f"{type(field_value)} is not supported")

    columns = [
        Column(k, get_type(v)(**get_type_constraints(v, k, ))) for k, v in d.items()
        if k not in [*ignore, "id"]
    ]

    return Table(
        name,
        _metadata,
        Column('id', Integer, primary_key=True),
        *columns
    )


