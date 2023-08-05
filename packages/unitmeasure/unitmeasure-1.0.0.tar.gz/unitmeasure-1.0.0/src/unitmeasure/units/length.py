from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitLength(dimension.Dimension):

    class Symbol(object):
        megameters = "Mm"
        kilometers = "km"
        hectometers = "hm"
        decameters = "dam"
        meters = "m"
        decimeters = "dm"
        centimeters = "cm"
        millimeters = "mm"
        micrometers = "µm"
        nanometers = "nm"
        picometers = "pm"
        inches = "in"
        feet = "ft"
        yards = "yd"
        miles = "mi"
        scandinavianMiles = "smi"
        lightyears = "ly"
        nauticalMiles = "NM"
        fathoms = "ftm"
        furlongs = "fur"
        astronomicalUnits = "ua"
        parsecs = "pc"

    class Coefficient(object):
        megameters = 1e6
        kilometers = 1e3
        hectometers = 1e2
        decameters = 1e1
        meters = 1.0
        decimeters = 1e-1
        centimeters = 1e-2
        millimeters = 1e-3
        micrometers = 1e-6
        nanometers = 1e-9
        picometers = 1e-12
        inches = 0.0254
        feet = 0.3048
        yards = 0.9144
        miles = 1609.34
        scandinavianMiles = 10000.0
        lightyears = 9.461e+15
        nauticalMiles = 1852.0
        fathoms = 1.8288
        furlongs = 201.168
        astronomicalUnits = 1.496e+11
        parsecs = 3.086e+16

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def megameters(cls):
        return UnitLength(cls.Symbol.megameters, cls.Coefficient.megameters)

    @classproperty
    def kilometers(cls):
        return UnitLength(cls.Symbol.kilometers, cls.Coefficient.kilometers)

    @classproperty
    def hectometers(cls):
        return UnitLength(cls.Symbol.hectometers, cls.Coefficient.hectometers)

    @classproperty
    def decameters(cls):
        return UnitLength(cls.Symbol.decameters, cls.Coefficient.decameters)

    @classproperty
    def meters(cls):
        return UnitLength(cls.Symbol.meters, cls.Coefficient.meters)

    @classproperty
    def decimeters(cls):
        return UnitLength(cls.Symbol.decimeters, cls.Coefficient.decimeters)

    @classproperty
    def centimeters(cls):
        return UnitLength(cls.Symbol.centimeters, cls.Coefficient.centimeters)

    @classproperty
    def millimeters(cls):
        return UnitLength(cls.Symbol.millimeters, cls.Coefficient.millimeters)

    @classproperty
    def micrometers(cls):
        return UnitLength(cls.Symbol.micrometers, cls.Coefficient.micrometers)

    @classproperty
    def nanometers(cls):
        return UnitLength(cls.Symbol.nanometers, cls.Coefficient.nanometers)

    @classproperty
    def picometers(cls):
        return UnitLength(cls.Symbol.picometers, cls.Coefficient.picometers)

    @classproperty
    def inches(cls):
        return UnitLength(cls.Symbol.inches, cls.Coefficient.inches)

    @classproperty
    def feet(cls):
        return UnitLength(cls.Symbol.feet, cls.Coefficient.feet)

    @classproperty
    def yards(cls):
        return UnitLength(cls.Symbol.yards, cls.Coefficient.yards)

    @classproperty
    def miles(cls):
        return UnitLength(cls.Symbol.miles, cls.Coefficient.miles)

    @classproperty
    def scandinavianMiles(cls):
        return UnitLength(cls.Symbol.scandinavianMiles,
                          cls.Coefficient.scandinavianMiles)

    @classproperty
    def lightyears(cls):
        return UnitLength(cls.Symbol.lightyears, cls.Coefficient.lightyears)

    @classproperty
    def nauticalMiles(cls):
        return UnitLength(cls.Symbol.nauticalMiles,
                          cls.Coefficient.nauticalMiles)

    @classproperty
    def fathoms(cls):
        return UnitLength(cls.Symbol.fathoms, cls.Coefficient.fathoms)

    @classproperty
    def furlongs(cls):
        return UnitLength(cls.Symbol.furlongs, cls.Coefficient.furlongs)

    @classproperty
    def astronomicalUnits(cls):
        return UnitLength(cls.Symbol.astronomicalUnits,
                          cls.Coefficient.astronomicalUnits)

    @classproperty
    def parsecs(cls):
        return UnitLength(cls.Symbol.parsecs, cls.Coefficient.parsecs)

    @classmethod
    def baseUnit(cls):
        return cls.meters

    def __eq__(self, other):
        if not isinstance(other, UnitLength):
            return False

        return super().__eq__(other)
