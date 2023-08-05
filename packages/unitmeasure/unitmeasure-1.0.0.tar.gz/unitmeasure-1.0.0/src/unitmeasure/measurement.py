import collections
import json
import numbers

from unitmeasure import dimension
from unitmeasure.unit import Unit


class Measurement(object):

    __slots__ = ["unit", "value"]

    def __init__(self, value, unit):
        super().__setattr__("value", value)
        super().__setattr__("unit", unit)

    def __setattr__(self, *args):
        raise TypeError("'Measurement' object doesn't support item assignment")

    def __delattr__(self, *args):
        raise TypeError("'Measurement' object doesn't support item deletion")

    @property
    def description(self):
        return f"{self.value} {self.unit.symbol}"

    @property
    def debugDescription(self):
        return f"{self.value} {self.unit.symbol}"

    def converted(self, otherUnit):
        """Returns a new measurement createdby converting to the provided unit.

        Args:
            otherUnit: a unit of the same `Dimension`

        Returns: 
            A converted measurement
        """
        if not isinstance(self.unit, dimension.Dimension):
            raise TypeError(
                "unit must be a Dimension to be able to convert between the kinds of units in a dimension"
            )
        if self.unit == otherUnit:
            return Measurement(self.value, self.unit)
        value_in_base = self.unit.converter.baseUnitValue(self.value)
        if otherUnit == self.unit.baseUnit():
            return Measurement(value_in_base, otherUnit)
        other_value_from_base = otherUnit.converter.value(value_in_base)
        return Measurement(other_value_from_base, otherUnit)

    def convert(self, otherUnit):
        temp = self.converted(otherUnit)
        super().__setattr__("value", temp.value)
        super().__setattr__("unit", temp.unit)

    def __add__(self, other):
        try:
            if self.unit == other.unit:
                return Measurement(self.value + other.value, self.unit)
            if isinstance(self.unit, dimension.Dimension) and isinstance(
                    other.unit, dimension.Dimension):
                if self.unit.baseUnit() == other.unit.baseUnit():
                    value_in_base = self.unit.converter.baseUnitValue(
                        self.value)
                    other_value_in_base = other.unit.converter.baseUnitValue(
                        other.value)
                    return Measurement(value_in_base + other_value_in_base,
                                       self.unit.baseUnit())
            raise TypeError(
                "Attempt to add measurements with non-equal dimensions")
        except AttributeError:
            raise TypeError(
                "cannot add value of type '{0}' to measurement".format(
                    type(other)))

    def __sub__(self, other):
        try:
            if self.unit == other.unit:
                return Measurement(self.value - other.value, self.unit)
            if isinstance(self.unit, dimension.Dimension) and isinstance(
                    other.unit, dimension.Dimension):
                if self.unit.baseUnit() == other.unit.baseUnit():
                    value_in_base = self.unit.converter.baseUnitValue(
                        self.value)
                    other_value_in_base = other.unit.converter.baseUnitValue(
                        other.value)
                    return Measurement(value_in_base - other_value_in_base,
                                       self.unit.baseUnit())
            raise TypeError(
                "Attempt to subtract measurements with non-equal dimensions")
        except AttributeError:
            raise TypeError(
                "cannot subtract value of type '{0}' to measurement".format(
                    type(other)))

    def __mul__(self, other):
        """Multiply a measurement by a scalar value"""
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "cannot multiply value of type '{0}' to measurement. value must be a number"
                .format(type(other)))
        return Measurement(self.value * other, self.unit)

    def __rmul__(self, other):
        """Multiply a scalar value by a measurement"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Divide a measurement by a scalar value"""
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "cannot divide value of type '{0}' to measurement. value must be a number"
                .format(type(other)))
        return Measurement(self.value / other, self.unit)

    def __rtruediv__(self, other):
        """Divide a scalar value by a measurement"""
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "cannot divide value of type '{0}' to measurement. value must be a number"
                .format(type(other)))
        return Measurement(other / self.value, self.unit)

    def __floordiv__(self, other):
        """Divide a measurement by a scalar value"""
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "cannot divide value of type '{0}' to measurement. value must be a number"
                .format(type(other)))
        return Measurement(self.value // other, self.unit)

    def __rfloordiv__(self, other):
        """Divide a scalar value by a measurement"""
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "cannot divide value of type '{0}' to measurement. value must be a number"
                .format(type(other)))
        return Measurement(other // self.value, self.unit)

    def __hash__(self):
        # WARNING: This needs to be kept in sync with __eq__
        # or hashing will break
        if isinstance(self.unit, dimension.Dimension):
            return hash((self.unit.converter.baseUnitValue(self.value),
                         self.unit.baseUnit().symbol))
        return hash((self.value, self.unit.symbol))

    def __eq__(self, other):
        if self.unit == other.unit:
            return self.value == other.value
        if isinstance(self.unit, dimension.Dimension) and isinstance(
                other.unit, dimension.Dimension):
            if self.unit.baseUnit() == other.unit.baseUnit():
                lhs_value_in_base = self.unit.converter.baseUnitValue(
                    self.value)
                rhs_value_in_base = other.unit.converter.baseUnitValue(
                    other.value)
                return lhs_value_in_base == rhs_value_in_base
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.unit == other.unit:
            return self.value < other.value
        if isinstance(self.unit, dimension.Dimension) and isinstance(
                other.unit, dimension.Dimension):
            if self.unit.baseUnit() == other.unit.baseUnit():
                lhs_value_in_base = self.unit.converter.baseUnitValue(
                    self.value)
                rhs_value_in_base = other.unit.converter.baseUnitValue(
                    other.value)
                return lhs_value_in_base < rhs_value_in_base
        raise TypeError(
            "Attempt to compare measurements with non-equal dimensions")

    def __le__(self, other):
        if self.unit == other.unit:
            return self.value <= other.value
        if isinstance(self.unit, dimension.Dimension) and isinstance(
                other.unit, dimension.Dimension):
            if self.unit.baseUnit() == other.unit.baseUnit():
                lhs_value_in_base = self.unit.converter.baseUnitValue(
                    self.value)
                rhs_value_in_base = other.unit.converter.baseUnitValue(
                    other.value)
                return lhs_value_in_base <= rhs_value_in_base
        raise TypeError(
            "Attempt to compare measurements with non-equal dimensions")

    def __gt__(self, other):
        if self.unit == other.unit:
            return self.value > other.value
        if isinstance(self.unit, dimension.Dimension) and isinstance(
                other.unit, dimension.Dimension):
            if self.unit.baseUnit() == other.unit.baseUnit():
                lhs_value_in_base = self.unit.converter.baseUnitValue(
                    self.value)
                rhs_value_in_base = other.unit.converter.baseUnitValue(
                    other.value)
                return lhs_value_in_base > rhs_value_in_base
        raise TypeError(
            "Attempt to compare measurements with non-equal dimensions")

    def __ge__(self, other):
        if self.unit == other.unit:
            return self.value >= other.value
        if isinstance(self.unit, dimension.Dimension) and isinstance(
                other.unit, dimension.Dimension):
            if self.unit.baseUnit() == other.unit.baseUnit():
                lhs_value_in_base = self.unit.converter.baseUnitValue(
                    self.value)
                rhs_value_in_base = other.unit.converter.baseUnitValue(
                    other.value)
                return lhs_value_in_base >= rhs_value_in_base
        raise TypeError(
            "Attempt to compare measurements with non-equal dimensions")

    def __repr__(self):
        return "{0}<{1}>".format(self.__class__.__name__,
                                 self.unit.__class__.__name__)

    def __str__(self):
        return self.description

    def to_json(self):
        data = collections.OrderedDict()
        data.update(json.loads(self.unit.to_json()))
        data.update({"value": self.value})
        return json.dumps(data, indent=4, default=float)
