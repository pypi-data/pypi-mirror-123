from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitAcceleration(dimension.Dimension):

    class Symbol(object):
        metersPerSecondSquared = "m/s²"
        gravity = "g"

    class Coefficient(object):
        metersPerSecondSquared = 1.0
        gravity = 9.81

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def metersPerSecondSquared(cls):
        return UnitAcceleration(cls.Symbol.metersPerSecondSquared,
                                cls.Coefficient.metersPerSecondSquared)

    @classproperty
    def gravity(cls):
        return UnitAcceleration(cls.Symbol.gravity, cls.Coefficient.gravity)

    @classmethod
    def baseUnit(cls):
        return cls.metersPerSecondSquared

    def __eq__(self, other):
        if not isinstance(other, UnitAcceleration):
            return False

        return super().__eq__(other)
