from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitFuelEfficiency(dimension.Dimension):

    class Symbol(object):
        litersPer100Kilometers = "L/100km"
        milesPerImperialGallon = "mpg"
        milesPerGallon = "mpg"

    class Coefficient(object):
        litersPer100Kilometers = 1.0
        milesPerImperialGallon = 282.481
        milesPerGallon = 235.215

    def __init__(self, symbol, reciprocal, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterReciprocal(reciprocal))

    @classproperty
    def litersPer100Kilometers(cls):
        return UnitFuelEfficiency(cls.Symbol.litersPer100Kilometers,
                                  cls.Coefficient.litersPer100Kilometers)

    @classproperty
    def milesPerImperialGallon(cls):
        return UnitFuelEfficiency(cls.Symbol.milesPerImperialGallon,
                                  cls.Coefficient.milesPerImperialGallon)

    @classproperty
    def milesPerGallon(cls):
        return UnitFuelEfficiency(cls.Symbol.milesPerGallon,
                                  cls.Coefficient.milesPerGallon)

    @classmethod
    def baseUnit(cls):
        return cls.litersPer100Kilometers

    def __eq__(self, other):
        if not isinstance(other, UnitFuelEfficiency):
            return False

        return super().__eq__(other)
