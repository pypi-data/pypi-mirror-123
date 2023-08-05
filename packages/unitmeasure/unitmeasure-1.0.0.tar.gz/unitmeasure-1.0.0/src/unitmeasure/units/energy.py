from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitEnergy(dimension.Dimension):

    class Symbol(object):
        kilojoules = "kJ"
        joules = "J"
        kilocalories = "kCal"
        calories = "cal"
        kilowattHours = "kWh"

    class Coefficient(object):
        kilojoules = 1e3
        joules = 1.0
        kilocalories = 4184.0
        calories = 4.184
        kilowattHours = 3600000.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def kilojoules(cls):
        return UnitEnergy(cls.Symbol.kilojoules, cls.Coefficient.kilojoules)

    @classproperty
    def joules(cls):
        return UnitEnergy(cls.Symbol.joules, cls.Coefficient.joules)

    @classproperty
    def kilocalories(cls):
        return UnitEnergy(cls.Symbol.kilocalories, cls.Coefficient.kilocalories)

    @classproperty
    def calories(cls):
        return UnitEnergy(cls.Symbol.calories, cls.Coefficient.calories)

    @classproperty
    def kilowattHours(cls):
        return UnitEnergy(cls.Symbol.kilowattHours,
                          cls.Coefficient.kilowattHours)

    @classmethod
    def baseUnit(cls):
        return cls.joules

    def __eq__(self, other):
        if not isinstance(other, UnitEnergy):
            return False

        return super().__eq__(other)
