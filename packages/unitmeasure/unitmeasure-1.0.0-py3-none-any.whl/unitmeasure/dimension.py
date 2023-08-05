import json

from unitmeasure import unit


class Dimension(unit.Unit):

    def __init__(self, symbol, converter):
        self.converter = converter
        super().__init__(symbol)

    @classmethod
    def baseUnit(cls):
        raise NotImplementedError(
            "you must override overide baseUnit in your class to define itsbase unit"
        )

    def __eq__(self, other):
        if not isinstance(other, Dimension):
            return False

        return super().__eq__(other) and self.converter == other.converter

    def to_json(self):
        data = json.loads(super().to_json())
        data["unit"]["converter"] = vars(self.converter)
        return json.dumps(data)
