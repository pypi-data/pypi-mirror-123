from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitArea(dimension.Dimension):

    class Symbol(object):
        squareMegameters = "Mm²"
        squareKilometers = "km²"
        squareMeters = "m²"
        squareCentimeters = "cm²"
        squareMillimeters = "mm²"
        squareMicrometers = "µm²"
        squareNanometers = "nm²"
        squareInches = "in²"
        squareFeet = "ft²"
        squareYards = "yd²"
        squareMiles = "mi²"
        acres = "ac"
        ares = "a"
        hectares = "ha"

    class Coefficient(object):
        squareMegameters = 1e12
        squareKilometers = 1e6
        squareMeters = 1.0
        squareCentimeters = 1e-4
        squareMillimeters = 1e-6
        squareMicrometers = 1e-12
        squareNanometers = 1e-18
        squareInches = 0.00064516
        squareFeet = 0.092903
        squareYards = 0.836127
        squareMiles = 2.59e+6
        acres = 4046.86
        ares = 100.0
        hectares = 10000.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def squareMegameters(cls):
        return UnitArea(cls.Symbol.squareMegameters,
                        cls.Coefficient.squareMegameters)

    @classproperty
    def squareKilometers(cls):
        return UnitArea(cls.Symbol.squareKilometers,
                        cls.Coefficient.squareKilometers)

    @classproperty
    def squareMeters(cls):
        return UnitArea(cls.Symbol.squareMeters, cls.Coefficient.squareMeters)

    @classproperty
    def squareCentimeters(cls):
        return UnitArea(cls.Symbol.squareCentimeters,
                        cls.Coefficient.squareCentimeters)

    @classproperty
    def squareMillimeters(cls):
        return UnitArea(cls.Symbol.squareMillimeters,
                        cls.Coefficient.squareMillimeters)

    @classproperty
    def squareMicrometers(cls):
        return UnitArea(cls.Symbol.squareMicrometers,
                        cls.Coefficient.squareMicrometers)

    @classproperty
    def squareNanometers(cls):
        return UnitArea(cls.Symbol.squareNanometers,
                        cls.Coefficient.squareNanometers)

    @classproperty
    def squareInches(cls):
        return UnitArea(cls.Symbol.squareInches, cls.Coefficient.squareInches)

    @classproperty
    def squareFeet(cls):
        return UnitArea(cls.Symbol.squareFeet, cls.Coefficient.squareFeet)

    @classproperty
    def squareYards(cls):
        return UnitArea(cls.Symbol.squareYards, cls.Coefficient.squareYards)

    @classproperty
    def squareMiles(cls):
        return UnitArea(cls.Symbol.squareMiles, cls.Coefficient.squareMiles)

    @classproperty
    def acres(cls):
        return UnitArea(cls.Symbol.acres, cls.Coefficient.acres)

    @classproperty
    def ares(cls):
        return UnitArea(cls.Symbol.ares, cls.Coefficient.ares)

    @classproperty
    def hectares(cls):
        return UnitArea(cls.Symbol.hectares, cls.Coefficient.hectares)

    @classmethod
    def baseUnit(cls):
        return cls.squareMeters

    def __eq__(self, other):
        if not isinstance(other, UnitArea):
            return False

        return super().__eq__(other)
