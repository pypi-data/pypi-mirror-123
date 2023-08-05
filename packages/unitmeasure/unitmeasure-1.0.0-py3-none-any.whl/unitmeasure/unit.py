import json


class Unit(object):

    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False

        return self.symbol == other.symbol

    def to_json(self):
        return json.dumps({"unit": {"symbol": self.symbol}}, indent=4)
