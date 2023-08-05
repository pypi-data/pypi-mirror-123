import math

from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitAngle(dimension.Dimension):

    class Symbol(object):
        degrees = "°"
        arcMinutes = "ʹ"
        arcSeconds = "ʹʹ"
        radians = "rad"
        gradians = "grad"
        revolutions = "rev"

    class Coefficient(object):
        degrees = 1.0
        arcMinutes = 1.0 / 60.0
        arcSeconds = 1.0 / 3600.0
        radians = 180.0 / math.pi
        gradians = 0.9
        revolutions = 360.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def degrees(cls):
        return UnitAngle(cls.Symbol.degrees, cls.Coefficient.degrees)

    @classproperty
    def arcMinutes(cls):
        return UnitAngle(cls.Symbol.arcMinutes, cls.Coefficient.arcMinutes)

    @classproperty
    def arcSeconds(cls):
        return UnitAngle(cls.Symbol.arcSeconds, cls.Coefficient.arcSeconds)

    @classproperty
    def radians(cls):
        return UnitAngle(cls.Symbol.radians, cls.Coefficient.radians)

    @classproperty
    def gradians(cls):
        return UnitAngle(cls.Symbol.gradians, cls.Coefficient.gradians)

    @classproperty
    def revolutions(cls):
        return UnitAngle(cls.Symbol.revolutions, cls.Coefficient.revolutions)

    @classmethod
    def baseUnit(cls):
        return cls.degrees

    def __eq__(self, other):
        if not isinstance(other, UnitAngle):
            return False

        return super().__eq__(other)
