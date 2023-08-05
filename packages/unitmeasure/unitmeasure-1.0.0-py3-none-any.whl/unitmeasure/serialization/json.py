import collections
import json
from typing import OrderedDict

from unitmeasure.measurement import Measurement
from unitmeasure.unit import Unit


def from_json(payload, dimension=None):
    data = json.loads(payload)
    if dimension is None:
        return Measurement(data["value"], Unit(data["unit"]["symbol"]))
    return Measurement(
        data["value"],
        dimension(data["unit"]["symbol"], **data["unit"]["converter"]))


def to_json(measurement):
    return measurement.to_json()
