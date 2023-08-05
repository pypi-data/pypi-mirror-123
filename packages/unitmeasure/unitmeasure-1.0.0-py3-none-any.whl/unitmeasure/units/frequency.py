from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitFrequency(dimension.Dimension):

    class Symbol(object):
        terahertz = "THz"
        gigahertz = "GHz"
        megahertz = "MHz"
        kilohertz = "kHz"
        hertz = "Hz"
        millihertz = "mHz"
        microhertz = "µHz"
        nanohertz = "nHz"

    class Coefficient(object):
        terahertz = 1e12
        gigahertz = 1e9
        megahertz = 1e6
        kilohertz = 1e3
        hertz = 1.0
        millihertz = 1e-3
        microhertz = 1e-6
        nanohertz = 1e-9

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def terahertz(cls):
        return UnitFrequency(cls.Symbol.terahertz, cls.Coefficient.terahertz)

    @classproperty
    def gigahertz(cls):
        return UnitFrequency(cls.Symbol.gigahertz, cls.Coefficient.gigahertz)

    @classproperty
    def megahertz(cls):
        return UnitFrequency(cls.Symbol.megahertz, cls.Coefficient.megahertz)

    @classproperty
    def kilohertz(cls):
        return UnitFrequency(cls.Symbol.kilohertz, cls.Coefficient.kilohertz)

    @classproperty
    def hertz(cls):
        return UnitFrequency(cls.Symbol.hertz, cls.Coefficient.hertz)

    @classproperty
    def millihertz(cls):
        return UnitFrequency(cls.Symbol.millihertz, cls.Coefficient.millihertz)

    @classproperty
    def microhertz(cls):
        return UnitFrequency(cls.Symbol.microhertz, cls.Coefficient.microhertz)

    @classproperty
    def nanohertz(cls):
        return UnitFrequency(cls.Symbol.nanohertz, cls.Coefficient.nanohertz)

    @classmethod
    def baseUnit(cls):
        return cls.hertz

    def __eq__(self, other):
        if not isinstance(other, UnitFrequency):
            return False

        return super().__eq__(other)
