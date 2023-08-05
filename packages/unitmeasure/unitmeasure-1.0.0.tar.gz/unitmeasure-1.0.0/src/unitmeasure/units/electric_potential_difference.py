from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitElectricPotentialDifference(dimension.Dimension):

    class Symbol(object):
        megavolts = "MV"
        kilovolts = "kV"
        volts = "V"
        millivolts = "mV"
        microvolts = "µV"

    class Coefficient(object):
        megavolts = 1e6
        kilovolts = 1e3
        volts = 1.0
        millivolts = 1e-3
        microvolts = 1e-6

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def megavolts(cls):
        return UnitElectricPotentialDifference(cls.Symbol.megavolts,
                                               cls.Coefficient.megavolts)

    @classproperty
    def kilovolts(cls):
        return UnitElectricPotentialDifference(cls.Symbol.kilovolts,
                                               cls.Coefficient.kilovolts)

    @classproperty
    def volts(cls):
        return UnitElectricPotentialDifference(cls.Symbol.volts,
                                               cls.Coefficient.volts)

    @classproperty
    def millivolts(cls):
        return UnitElectricPotentialDifference(cls.Symbol.millivolts,
                                               cls.Coefficient.millivolts)

    @classproperty
    def microvolts(cls):
        return UnitElectricPotentialDifference(cls.Symbol.microvolts,
                                               cls.Coefficient.microvolts)

    @classmethod
    def baseUnit(cls):
        return cls.volts

    def __eq__(self, other):
        if not isinstance(other, UnitElectricPotentialDifference):
            return False

        return super().__eq__(other)
