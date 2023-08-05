from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitDispersion(dimension.Dimension):

    class Symbol(object):
        partsPerMillion = "ppm"

    class Coefficient(object):
        partsPerMillion = 1.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def partsPerMillion(cls):
        return UnitDispersion(cls.Symbol.partsPerMillion,
                              cls.Coefficient.partsPerMillion)

    @classmethod
    def baseUnit(cls):
        return cls.partsPerMillion

    def __eq__(self, other):
        if not isinstance(other, UnitDispersion):
            return False

        return super().__eq__(other)
