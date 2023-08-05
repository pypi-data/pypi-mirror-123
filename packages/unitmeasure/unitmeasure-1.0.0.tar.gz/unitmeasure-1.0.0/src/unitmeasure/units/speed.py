from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitSpeed(dimension.Dimension):

    class Symbol(object):
        metersPerSecond = "m/s"
        kilometersPerHour = "km/h"
        milesPerHour = "mph"
        knots = "kn"

    class Coefficient(object):
        metersPerSecond = 1.0
        kilometersPerHour = 0.277778
        milesPerHour = 0.44704
        knots = 0.514444

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def metersPerSecond(cls):
        return UnitSpeed(cls.Symbol.metersPerSecond,
                         cls.Coefficient.metersPerSecond)

    @classproperty
    def kilometersPerHour(cls):
        return UnitSpeed(cls.Symbol.kilometersPerHour,
                         cls.Coefficient.kilometersPerHour)

    @classproperty
    def milesPerHour(cls):
        return UnitSpeed(cls.Symbol.milesPerHour, cls.Coefficient.milesPerHour)

    @classproperty
    def knots(cls):
        return UnitSpeed(cls.Symbol.knots, cls.Coefficient.knots)

    @classmethod
    def baseUnit(cls):
        return cls.metersPerSecond

    def __eq__(self, other):
        if not isinstance(other, UnitSpeed):
            return False

        return super().__eq__(other)
