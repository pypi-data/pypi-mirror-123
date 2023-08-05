from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitPower(dimension.Dimension):

    class Symbol(object):
        terawatts = "TW"
        gigawatts = "GW"
        megawatts = "MW"
        kilowatts = "kW"
        watts = "W"
        milliwatts = "mW"
        microwatts = "µW"
        nanowatts = "nW"
        picowatts = "pW"
        femtowatts = "fW"
        horsepower = "hp"

    class Coefficient(object):
        terawatts = 1e12
        gigawatts = 1e9
        megawatts = 1e6
        kilowatts = 1e3
        watts = 1.0
        milliwatts = 1e-3
        microwatts = 1e-6
        nanowatts = 1e-9
        picowatts = 1e-12
        femtowatts = 1e-15
        horsepower = 745.7

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def terawatts(cls):
        return UnitPower(cls.Symbol.terawatts, cls.Coefficient.terawatts)

    @classproperty
    def gigawatts(cls):
        return UnitPower(cls.Symbol.gigawatts, cls.Coefficient.gigawatts)

    @classproperty
    def megawatts(cls):
        return UnitPower(cls.Symbol.megawatts, cls.Coefficient.megawatts)

    @classproperty
    def kilowatts(cls):
        return UnitPower(cls.Symbol.kilowatts, cls.Coefficient.kilowatts)

    @classproperty
    def watts(cls):
        return UnitPower(cls.Symbol.watts, cls.Coefficient.watts)

    @classproperty
    def milliwatts(cls):
        return UnitPower(cls.Symbol.milliwatts, cls.Coefficient.milliwatts)

    @classproperty
    def microwatts(cls):
        return UnitPower(cls.Symbol.microwatts, cls.Coefficient.microwatts)

    @classproperty
    def nanowatts(cls):
        return UnitPower(cls.Symbol.nanowatts, cls.Coefficient.nanowatts)

    @classproperty
    def picowatts(cls):
        return UnitPower(cls.Symbol.picowatts, cls.Coefficient.picowatts)

    @classproperty
    def femtowatts(cls):
        return UnitPower(cls.Symbol.femtowatts, cls.Coefficient.femtowatts)

    @classproperty
    def horsepower(cls):
        return UnitPower(cls.Symbol.horsepower, cls.Coefficient.horsepower)

    @classmethod
    def baseUnit(cls):
        return cls.watts

    def __eq__(self, other):
        if not isinstance(other, UnitPower):
            return False

        return super().__eq__(other)
