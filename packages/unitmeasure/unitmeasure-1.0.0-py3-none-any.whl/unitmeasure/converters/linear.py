from unitmeasure.converters import model


class UnitConverterLinear(model.UnitConverter):

    def __init__(self, coefficient, constant=0):
        self.coefficient = coefficient
        self.constant = constant

    def baseUnitValue(self, value):
        return value * self.coefficient + self.constant

    def value(self, baseUnitValue):
        return (baseUnitValue - self.constant) / self.coefficient

    def __eq__(self, other):
        if not isinstance(other, UnitConverterLinear):
            return False

        return self.coefficient == other.coefficient and self.constant == other.constant
