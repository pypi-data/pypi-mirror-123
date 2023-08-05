from unitmeasure.converters import model


class UnitConverterReciprocal(model.UnitConverter):

    def __init__(self, reciprocal):
        self.reciprocal = reciprocal

    def baseUnitValue(self, value):
        return self.reciprocal / value

    def value(self, baseUnitValue):
        return self.reciprocal / baseUnitValue

    def __eq__(self, other):
        if not isinstance(other, UnitConverterReciprocal):
            return False

        return self.reciprocal == other.reciprocal