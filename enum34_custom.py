from enum import Enum, EnumMeta
from functools import total_ordering


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        enum_class = super().__new__(metacls, cls, bases, classdict)

        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member.value, tuple):
                raise TypeError('{} = {!r}, should be tuple!'
                                .format(member.name, member.value))
        return enum_class

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed."""

        for member in cls:
            if value in member.value:
                return member

        # raise ValueError otherwise
        return super().__call__(value)


class MultiValueEnum(Enum, metaclass=_MultiMeta):
    """Enum subclass where members are declared as tuples."""


@total_ordering
class OrderableMixin:
    """Mixin for comparable Enums. The order is the definition order
    from smaller to bigger.
    """

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self.name) < names.index(other.name)
        return NotImplemented
