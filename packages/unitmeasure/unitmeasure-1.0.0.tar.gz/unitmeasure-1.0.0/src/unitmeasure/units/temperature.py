from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitTemperature(dimension.Dimension):

    class Symbol(object):
        kelvin = "K"
        celsius = "°C"
        fahrenheit = "°F"

    class Coefficient(object):
        kelvin = 1.0
        celsius = 1.0
        fahrenheit = 0.55555555555556

    class Constant(object):
        kelvin = 0.0
        celsius = 273.15
        fahrenheit = 255.37222222222427

    def __init__(self, symbol, coefficient, constant, *args, **kwargs):
        super().__init__(
            symbol,
            converters.UnitConverterLinear(coefficient, constant=constant))

    @classproperty
    def kelvin(cls):
        return UnitTemperature(cls.Symbol.kelvin, cls.Coefficient.kelvin,
                               cls.Constant.kelvin)

    @classproperty
    def celsius(cls):
        return UnitTemperature(cls.Symbol.celsius, cls.Coefficient.celsius,
                               cls.Constant.celsius)

    @classproperty
    def fahrenheit(cls):
        return UnitTemperature(cls.Symbol.fahrenheit,
                               cls.Coefficient.fahrenheit,
                               cls.Constant.fahrenheit)

    @classmethod
    def baseUnit(cls):
        return cls.kelvin

    def __eq__(self, other):
        if not isinstance(other, UnitTemperature):
            return False

        return super().__eq__(other)
