from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitVolume(dimension.Dimension):

    class Symbol(object):
        megaliters = "ML"
        kiloliters = "kL"
        liters = "L"
        deciliters = "dl"
        centiliters = "cL"
        milliliters = "mL"
        cubicKilometers = "km³"
        cubicMeters = "m³"
        cubicDecimeters = "dm³"
        cubicCentimeters = "cm³"
        cubicMillimeters = "mm³"
        cubicInches = "in³"
        cubicFeet = "ft³"
        cubicYards = "yd³"
        cubicMiles = "mi³"
        acreFeet = "af"
        bushels = "bsh"
        teaspoons = "tsp"
        tablespoons = "tbsp"
        fluidOunces = "fl oz"
        cups = "cup"
        pints = "pt"
        quarts = "qt"
        gallons = "gal"
        imperialTeaspoons = "tsp Imperial"
        imperialTablespoons = "tbsp Imperial"
        imperialFluidOunces = "fl oz Imperial"
        imperialPints = "pt Imperial"
        imperialQuarts = "qt Imperial"
        imperialGallons = "gal Imperial"
        metricCups = "metric cup Imperial"

    class Coefficient(object):
        megaliters = 1e6
        kiloliters = 1e3
        liters = 1.0
        deciliters = 1e-1
        centiliters = 1e-2
        milliliters = 1e-3
        cubicKilometers = 1e12
        cubicMeters = 1000.0
        cubicDecimeters = 1.0
        cubicCentimeters = 1e-3
        cubicMillimeters = 1e-6
        cubicInches = 0.0163871
        cubicFeet = 28.3168
        cubicYards = 764.555
        cubicMiles = 4.168e+12
        acreFeet = 1.233e+6
        bushels = 35.2391
        teaspoons = 0.00492892
        tablespoons = 0.0147868
        fluidOunces = 0.0295735
        cups = 0.24
        pints = 0.473176
        quarts = 0.946353
        gallons = 3.78541
        imperialTeaspoons = 0.00591939
        imperialTablespoons = 0.0177582
        imperialFluidOunces = 0.0284131
        imperialPints = 0.568261
        imperialQuarts = 1.13652
        imperialGallons = 4.54609
        metricCups = 0.25

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def megaliters(cls):
        return UnitVolume(cls.Symbol.megaliters, cls.Coefficient.megaliters)

    @classproperty
    def kiloliters(cls):
        return UnitVolume(cls.Symbol.kiloliters, cls.Coefficient.kiloliters)

    @classproperty
    def liters(cls):
        return UnitVolume(cls.Symbol.liters, cls.Coefficient.liters)

    @classproperty
    def deciliters(cls):
        return UnitVolume(cls.Symbol.deciliters, cls.Coefficient.deciliters)

    @classproperty
    def centiliters(cls):
        return UnitVolume(cls.Symbol.centiliters, cls.Coefficient.centiliters)

    @classproperty
    def milliliters(cls):
        return UnitVolume(cls.Symbol.milliliters, cls.Coefficient.milliliters)

    @classproperty
    def cubicKilometers(cls):
        return UnitVolume(cls.Symbol.cubicKilometers,
                          cls.Coefficient.cubicKilometers)

    @classproperty
    def cubicMeters(cls):
        return UnitVolume(cls.Symbol.cubicMeters, cls.Coefficient.cubicMeters)

    @classproperty
    def cubicDecimeters(cls):
        return UnitVolume(cls.Symbol.cubicDecimeters,
                          cls.Coefficient.cubicDecimeters)

    @classproperty
    def cubicCentimeters(cls):
        return UnitVolume(cls.Symbol.cubicCentimeters,
                          cls.Coefficient.cubicCentimeters)

    @classproperty
    def cubicMillimeters(cls):
        return UnitVolume(cls.Symbol.cubicMillimeters,
                          cls.Coefficient.cubicMillimeters)

    @classproperty
    def cubicInches(cls):
        return UnitVolume(cls.Symbol.cubicInches, cls.Coefficient.cubicInches)

    @classproperty
    def cubicFeet(cls):
        return UnitVolume(cls.Symbol.cubicFeet, cls.Coefficient.cubicFeet)

    @classproperty
    def cubicYards(cls):
        return UnitVolume(cls.Symbol.cubicYards, cls.Coefficient.cubicYards)

    @classproperty
    def cubicMiles(cls):
        return UnitVolume(cls.Symbol.cubicMiles, cls.Coefficient.cubicMiles)

    @classproperty
    def acreFeet(cls):

        return UnitVolume(cls.Symbol.acreFeet, cls.Coefficient.acreFeet)

    @classproperty
    def bushels(cls):

        return UnitVolume(cls.Symbol.bushels, cls.Coefficient.bushels)

    @classproperty
    def teaspoons(cls):

        return UnitVolume(cls.Symbol.teaspoons, cls.Coefficient.teaspoons)

    @classproperty
    def tablespoons(cls):
        return UnitVolume(cls.Symbol.tablespoons, cls.Coefficient.tablespoons)

    @classproperty
    def fluidOunces(cls):
        return UnitVolume(cls.Symbol.fluidOunces, cls.Coefficient.fluidOunces)

    @classproperty
    def cups(cls):
        return UnitVolume(cls.Symbol.cups, cls.Coefficient.cups)

    @classproperty
    def pints(cls):
        return UnitVolume(cls.Symbol.pints, cls.Coefficient.pints)

    @classproperty
    def quarts(cls):
        return UnitVolume(cls.Symbol.quarts, cls.Coefficient.quarts)

    @classproperty
    def gallons(cls):
        return UnitVolume(cls.Symbol.gallons, cls.Coefficient.gallons)

    @classproperty
    def imperialTeaspoons(cls):
        return UnitVolume(cls.Symbol.imperialTeaspoons,
                          cls.Coefficient.imperialTeaspoons)

    @classproperty
    def imperialTablespoons(cls):
        return UnitVolume(cls.Symbol.imperialTablespoons,
                          cls.Coefficient.imperialTablespoons)

    @classproperty
    def imperialFluidOunces(cls):
        return UnitVolume(cls.Symbol.imperialFluidOunces,
                          cls.Coefficient.imperialFluidOunces)

    @classproperty
    def imperialPints(cls):
        return UnitVolume(cls.Symbol.imperialPints,
                          cls.Coefficient.imperialPints)

    @classproperty
    def imperialQuarts(cls):
        return UnitVolume(cls.Symbol.imperialQuarts,
                          cls.Coefficient.imperialQuarts)

    @classproperty
    def imperialGallons(cls):
        return UnitVolume(cls.Symbol.imperialGallons,
                          cls.Coefficient.imperialGallons)

    @classproperty
    def metricCups(cls):
        return UnitVolume(cls.Symbol.metricCups, cls.Coefficient.metricCups)

    @classmethod
    def baseUnit(cls):
        return cls.liters

    def __eq__(self, other):
        if not isinstance(other, UnitVolume):
            return False

        return super().__eq__(other)
