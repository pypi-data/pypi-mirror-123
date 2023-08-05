from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitElectricResistance(dimension.Dimension):

    class Symbol(object):
        megaohms = "MΩ"
        kiloohms = "kΩ"
        ohms = "Ω"
        milliohms = "mΩ"
        microohms = "µΩ"

    class Coefficient(object):
        megaohms = 1e6
        kiloohms = 1e3
        ohms = 1.0
        milliohms = 1e-3
        microohms = 1e-6

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def megaohms(cls):
        return UnitElectricResistance(cls.Symbol.megaohms,
                                      cls.Coefficient.megaohms)

    @classproperty
    def kiloohms(cls):
        return UnitElectricResistance(cls.Symbol.kiloohms,
                                      cls.Coefficient.kiloohms)

    @classproperty
    def ohms(cls):
        return UnitElectricResistance(cls.Symbol.ohms, cls.Coefficient.ohms)

    @classproperty
    def milliohms(cls):
        return UnitElectricResistance(cls.Symbol.milliohms,
                                      cls.Coefficient.milliohms)

    @classproperty
    def microohms(cls):
        return UnitElectricResistance(cls.Symbol.microohms,
                                      cls.Coefficient.microohms)

    @classmethod
    def baseUnit(cls):
        return cls.ohms

    def __eq__(self, other):
        if not isinstance(other, UnitElectricResistance):
            return False

        return super().__eq__(other)
