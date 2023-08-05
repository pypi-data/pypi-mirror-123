from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitIlluminance(dimension.Dimension):

    class Symbol(object):
        lux = "lx"

    class Coefficient(object):
        lux = 1.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def lux(cls):
        return UnitIlluminance(cls.Symbol.lux, cls.Coefficient.lux)

    @classmethod
    def baseUnit(cls):
        return cls.lux

    def __eq__(self, other):
        if not isinstance(other, UnitIlluminance):
            return False

        return super().__eq__(other)
