import os
from dataclasses import dataclass
from json import loads
from typing import Dict, List, Any, Tuple, Optional

import requests

from dizzle.fun import (
    Option,
    getter,
    item_getter,
    stop_chain,
    has_keys,
    returner,
    kwargs_unwrapper,
    identity,
)


@dataclass
class Location:
    lat: float
    lng: float


def geocode(address: str, type_: str = "json", api_key: str = None):
    if not api_key:
        api_key = os.environ.get("GEOCODING_API_KEY")
    return requests.get(
        f"https://maps.googleapis.com/maps/api/geocode/{type_}?address={address}&key={api_key}"
    )


def geocode_json(
    path: str,
    *include: str,
    api_key: str = None,
    **includes_fn,
) -> Tuple[List[Dict], List[Dict]]:
    """
    :param path:
    :param include:
    :param api_key:
    :return:
    """
    if not api_key:
        api_key = os.environ.get("GEOCODING_API_KEY")
    could_not_resolve = []
    results = []
    with open(path) as f:
        content = f.read()
        obj = loads(content)
        for entry in obj:
            street = " ".join(
                (
                    str(includes_fn.get(val, identity)(entry.get(val)))
                    for val in include
                    if val in entry
                )
            )
            res = geocode(street, api_key=api_key)
            try:
                res.raise_for_status()
                location = extract_lat_lng(res.json())
                if not location:
                    could_not_resolve.append(entry)
                    continue
                entry: Dict
                results.append({**entry, "lat": location.lat, "lng": location.lng})
            except BaseException:
                could_not_resolve.append(entry)
                continue
        return results, could_not_resolve


def extract_lat_lng(res: Dict) -> Optional[Location]:
    take_result = getter("results")
    take_first = item_getter(0)
    take_geometry = getter("geometry")
    take_location = getter("location")

    option = Option(res)
    with stop_chain(
        option,
        take_result,
        take_first,
        take_geometry,
        take_location,
    ) as o:
        return o.condition(
            has_keys("lat", "lng"), kwargs_unwrapper(Location), returner(None)
        )
