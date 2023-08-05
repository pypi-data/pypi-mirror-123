from unitmeasure import converters
from unitmeasure import dimension

from unitmeasure.util import classproperty


class UnitConcentrationMass(dimension.Dimension):

    class Symbol(object):
        gramsPerLiter = "g/L"
        milligramsPerDeciliter = "mg/dL"
        millimolesPerLiter = "mmol/L"

    class Coefficient(object):
        gramsPerLiter = 1.0
        milligramsPerDeciliter = 0.01
        millimolesPerLiter = 18.0

    def __init__(self, symbol, coefficient, *args, **kwargs):
        super().__init__(symbol, converters.UnitConverterLinear(coefficient))

    @classproperty
    def gramsPerLiter(cls):
        return UnitConcentrationMass(cls.Symbol.gramsPerLiter,
                                     cls.Coefficient.gramsPerLiter)

    @classproperty
    def milligramsPerDeciliter(cls):
        return UnitConcentrationMass(cls.Symbol.milligramsPerDeciliter,
                                     cls.Coefficient.milligramsPerDeciliter)

    @classmethod
    def millimolesPerLiter(cls, gramsPerMole):
        return UnitConcentrationMass(
            cls.Symbol.millimolesPerLiter,
            cls.Coefficient.millimolesPerLiter * gramsPerMole)

    @classmethod
    def baseUnit(cls):
        return cls.gramsPerLiter

    def __eq__(self, other):
        if not isinstance(other, UnitConcentrationMass):
            return False

        return super().__eq__(other)