from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitMass(dimension.Dimension):

    class Symbol(object):
        kilograms = "kg"
        grams = "g"
        decigrams = "dg"
        centigrams = "cg"
        milligrams = "mg"
        micrograms = "µg"
        nanograms = "ng"
        picograms = "pg"
        ounces = "oz"
        pounds = "lb"
        stones = "st"
        metricTons = "t"
        shortTons = "ton"
        carats = "ct"
        ouncesTroy = "oz t"
        slugs = "slug"

    class Coefficient(object):
        kilograms = 1.0
        grams = 1e-3
        decigrams = 1e-4
        centigrams = 1e-5
        milligrams = 1e-6
        micrograms = 1e-9
        nanograms = 1e-12
        picograms = 1e-15
        ounces = 0.0283495
        pounds = 0.453592
        stones = 0.157473
        metricTons = 1000.0
        shortTons = 907.185
        carats = 0.0002
        ouncesTroy = 0.03110348
        slugs = 14.5939

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def kilograms(cls):
        return UnitMass(cls.Symbol.kilograms, cls.Coefficient.kilograms)

    @classproperty
    def grams(cls):
        return UnitMass(cls.Symbol.grams, cls.Coefficient.grams)

    @classproperty
    def decigrams(cls):
        return UnitMass(cls.Symbol.decigrams, cls.Coefficient.decigrams)

    @classproperty
    def centigrams(cls):
        return UnitMass(cls.Symbol.centigrams, cls.Coefficient.centigrams)

    @classproperty
    def milligrams(cls):
        return UnitMass(cls.Symbol.milligrams, cls.Coefficient.milligrams)

    @classproperty
    def micrograms(cls):
        return UnitMass(cls.Symbol.micrograms, cls.Coefficient.micrograms)

    @classproperty
    def nanograms(cls):
        return UnitMass(cls.Symbol.nanograms, cls.Coefficient.nanograms)

    @classproperty
    def picograms(cls):
        return UnitMass(cls.Symbol.picograms, cls.Coefficient.picograms)

    @classproperty
    def ounces(cls):
        return UnitMass(cls.Symbol.ounces, cls.Coefficient.ounces)

    @classproperty
    def pounds(cls):
        return UnitMass(cls.Symbol.pounds, cls.Coefficient.pounds)

    @classproperty
    def stones(cls):
        return UnitMass(cls.Symbol.stones, cls.Coefficient.stones)

    @classproperty
    def metricTons(cls):
        return UnitMass(cls.Symbol.metricTons, cls.Coefficient.metricTons)

    @classproperty
    def shortTons(cls):
        return UnitMass(cls.Symbol.shortTons, cls.Coefficient.shortTons)

    @classproperty
    def carats(cls):
        return UnitMass(cls.Symbol.carats, cls.Coefficient.carats)

    @classproperty
    def ouncesTroy(cls):
        return UnitMass(cls.Symbol.ouncesTroy, cls.Coefficient.ouncesTroy)

    @classproperty
    def slugs(cls):
        return UnitMass(cls.Symbol.slugs, cls.Coefficient.slugs)

    @classmethod
    def baseUnit(cls):
        return cls.kilograms

    def __eq__(self, other):
        if not isinstance(other, UnitMass):
            return False

        return super().__eq__(other)
