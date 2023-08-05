from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitPressure(dimension.Dimension):

    class Symbol(object):
        newtonsPerMetersSquared = "N/m²"
        gigapascals = "GPa"
        megapascals = "MPa"
        kilopascals = "kPa"
        hectopascals = "hPa"
        inchesOfMercury = "inHg"
        bars = "bar"
        millibars = "mbar"
        millimetersOfMercury = "mmHg"
        poundsForcePerSquareInch = "psi"

    class Coefficient(object):
        newtonsPerMetersSquared = 1.0
        gigapascals = 1e9
        megapascals = 1e6
        kilopascals = 1e3
        hectopascals = 1e2
        inchesOfMercury = 3386.39
        bars = 1e5
        millibars = 1e2
        millimetersOfMercury = 133.322
        poundsForcePerSquareInch = 6894.76

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def newtonsPerMetersSquared(cls):
        return UnitPressure(cls.Symbol.newtonsPerMetersSquared,
                            cls.Coefficient.newtonsPerMetersSquared)

    @classproperty
    def gigapascals(cls):
        return UnitPressure(cls.Symbol.gigapascals, cls.Coefficient.gigapascals)

    @classproperty
    def megapascals(cls):
        return UnitPressure(cls.Symbol.megapascals, cls.Coefficient.megapascals)

    @classproperty
    def kilopascals(cls):
        return UnitPressure(cls.Symbol.kilopascals, cls.Coefficient.kilopascals)

    @classproperty
    def hectopascals(cls):
        return UnitPressure(cls.Symbol.hectopascals,
                            cls.Coefficient.hectopascals)

    @classproperty
    def inchesOfMercury(cls):
        return UnitPressure(cls.Symbol.inchesOfMercury,
                            cls.Coefficient.inchesOfMercury)

    @classproperty
    def bars(cls):
        return UnitPressure(cls.Symbol.bars, cls.Coefficient.bars)

    @classproperty
    def millibars(cls):
        return UnitPressure(cls.Symbol.millibars, cls.Coefficient.millibars)

    @classproperty
    def millimetersOfMercury(cls):
        return UnitPressure(cls.Symbol.millimetersOfMercury,
                            cls.Coefficient.millimetersOfMercury)

    @classproperty
    def poundsForcePerSquareInch(cls):
        return UnitPressure(cls.Symbol.poundsForcePerSquareInch,
                            cls.Coefficient.poundsForcePerSquareInch)

    @classmethod
    def baseUnit(cls):
        return cls.newtonsPerMetersSquared

    def __eq__(self, other):
        if not isinstance(other, UnitPressure):
            return False

        return super().__eq__(other)
