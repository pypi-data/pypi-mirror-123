from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitDuration(dimension.Dimension):

    class Symbol(object):
        seconds = "s"
        minutes = "m"
        hours = "h"

    class Coefficient(object):
        seconds = 1.0
        minutes = 60.0
        hours = 3600.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def seconds(cls):
        return UnitDuration(cls.Symbol.seconds, cls.Coefficient.seconds)

    @classproperty
    def minutes(cls):
        return UnitDuration(cls.Symbol.minutes, cls.Coefficient.minutes)

    @classproperty
    def hours(cls):
        return UnitDuration(cls.Symbol.hours, cls.Coefficient.hours)

    @classmethod
    def baseUnit(cls):
        return cls.seconds

    def __eq__(self, other):
        if not isinstance(other, UnitDuration):
            return False

        return super().__eq__(other)
