from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitElectricCharge(dimension.Dimension):

    class Symbol(object):
        coulombs = "C"
        megaampereHours = "MAh"
        kiloampereHours = "kAh"
        ampereHours = "Ah"
        milliampereHours = "mAh"
        microampereHours = "µAh"

    class Coefficient(object):
        coulombs = 1.0
        megaampereHours = 3.6e9
        kiloampereHours = 3600000.0
        ampereHours = 3600.0
        milliampereHours = 3.6
        microampereHours = 0.0036

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def coulombs(cls):
        return UnitElectricCharge(cls.Symbol.coulombs, cls.Coefficient.coulombs)

    @classproperty
    def megaampereHours(cls):
        return UnitElectricCharge(cls.Symbol.megaampereHours,
                                  cls.Coefficient.megaampereHours)

    @classproperty
    def kiloampereHours(cls):
        return UnitElectricCharge(cls.Symbol.kiloampereHours,
                                  cls.Coefficient.kiloampereHours)

    @classproperty
    def ampereHours(cls):
        return UnitElectricCharge(cls.Symbol.ampereHours,
                                  cls.Coefficient.ampereHours)

    @classproperty
    def milliampereHours(cls):
        return UnitElectricCharge(cls.Symbol.milliampereHours,
                                  cls.Coefficient.milliampereHours)

    @classproperty
    def microampereHours(cls):
        return UnitElectricCharge(cls.Symbol.microampereHours,
                                  cls.Coefficient.microampereHours)

    @classmethod
    def baseUnit(cls):
        return cls.coulombs

    def __eq__(self, other):
        if not isinstance(other, UnitElectricCharge):
            return False

        return super().__eq__(other)
