from enum import (
    Enum, EnumMeta, _EnumDict, _is_sunder, _is_dunder, _is_descriptor
)
from functools import total_ordering


__version__ = '0.4.0'
__all__ = ['MultiValueEnum', 'StrEnum', 'CaseInsensitiveStrEnum']


class _MultiValueMeta(EnumMeta):
    def __init__(self, cls, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            if not isinstance(member.value, tuple):
                raise TypeError('{} = {!r}, should be tuple!'
                                .format(member.name, member.value))

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed."""
        for member in cls:
            if value in member.value:
                return member
        else:
            raise ValueError("%s is not a valid %s" % (value, cls.__name__))


class MultiValueEnum(Enum, metaclass=_MultiValueMeta):
    """Enum subclass where members can have multiple values.
    You can reference a member by any of its value in the associated tuple.
    """


class _CheckTypeDict(_EnumDict):
    def __init__(self, expected_type):
        super().__init__()
        self._expected_type = expected_type

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if not isinstance(value, self._expected_type):
            raise TypeError('{} = {!r}, should be {}!'.format(
                            key, value, self._expected_type)
            )


class _CheckTypeEnumMeta(EnumMeta):
    @classmethod
    def __prepare__(metacls, cls, bases):
        if bases[-1] == Enum:
            # basic stdlib Enum
            return _EnumDict()
        else:
            # User subclassed one of our custom Enum,
            # so the last in the mro will be that class
            # __mro__ of our custom Enum class:
            # 1. subclass (e.g. StrEnum or IntEnum)
            # 2. expected type (e.g. str)
            # 3. Enum class
            # 4. object
            our_enum_class = bases[-1]
            expected_type = our_enum_class.__mro__[1]
            return _CheckTypeDict(expected_type)


class StrEnum(str, Enum, metaclass=_CheckTypeEnumMeta):
    """Enum subclass which members are also instances of str
    and directly comparable to strings. str type is forced at declaration.
    """


class _CaseInsensitiveEnumMeta(_CheckTypeEnumMeta):
    def __init__(self, cls, bases, classdict):
        for name, member in self._member_map_.items():
            self._value2member_map_.pop(member.value)
            member._value_ = member.value.upper()
            # need to update also
            self._value2member_map_[member.value] = member

    def __call__(cls, value):
        return cls.__new__(cls, value.upper())


class CaseInsensitiveStrEnum(str, Enum, metaclass=_CaseInsensitiveEnumMeta):
    def __new__(cls, *args):
        args = tuple(arg.upper() for arg in args if isinstance(arg, str))
        return super().__new__(cls, *args)

    def __eq__(self, other):
        return self.upper() == other.upper()


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
