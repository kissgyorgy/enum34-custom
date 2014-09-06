from enum import Enum, EnumMeta, _EnumDict
from functools import total_ordering
from collections import Iterable


__version__ = '0.6.0'
__all__ = ['MultiValueEnum', 'no_overlap', 'StrEnum', 'CaseInsensitiveStrEnum',
           'CaseInsensitiveMultiValueEnum']


class _MultiValueMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            val = member._value_
            if not isinstance(val, Iterable) or type(val) == str:
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                    .format(member._name_, val, type(val))
                )
            # set is faster to lookup
            member._lookup_set_ = set(val)

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed."""
        for member in cls:
            if value in member._lookup_set_:
                return member
        else:
            # lookup by original value, enum instance, or raise ValueError
            return super().__call__(value)


class MultiValueEnum(Enum, metaclass=_MultiValueMeta):
    """Enum subclass where a member can be any iterable (except str).
    You can reference a member by any of its element in the associated iterable.
    """


class _CasInsensitiveMultiValueMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            val = member._value_
            if not isinstance(val, Iterable) or type(val) == str:
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                    .format(member._name_, val, type(val))
                )
            # set is faster to lookup
            member._lookup_set_ = set()
            for elem in val:
                if type(elem) == str:
                    elem = elem.upper()
                member._lookup_set_.add(elem)

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed."""
        compare = value.upper() if type(value) is str else value
        for member in cls:
            if compare in member._lookup_set_:
                return member
        else:
            # lookup by original value, enum instance, or raise ValueError
            return super().__call__(value)


class CaseInsensitiveMultiValueEnum(
    Enum, metaclass=_CasInsensitiveMultiValueMeta):
    """Same as MultiValueEnum, except when member value contains an str,
    they will be compared in a case-insensitive manner. Non-str types left
    untouched.
    """


def no_overlap(multienum):
    """Class decorator for MultiValueEnum ensuring non overlapping elements
    in member values. Other words: ensure no element in any member value is
    present in any other member value.
    """
    duplicates = []
    members = []

    for member in multienum.__members__.values():
        for prev_member in members:
            intersection = member._lookup_set_ & prev_member._lookup_set_
            if intersection:
                duplicates.append(
                    (member._name_, prev_member._name_, intersection)
                )
        members.append(member)

    if duplicates:
        alias_details = ', '.join(["{} & {} -> {}"
                                  .format(alias, name, intersection) for
                                  (alias, name, intersection) in duplicates])
        raise ValueError('common element found in {!r}: {}'
                         .format(multienum, alias_details))
    return multienum


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
            self._value2member_map_.pop(member._value_)
            member._value_ = member.value.upper()
            # need to update also
            self._value2member_map_[member._value_] = member

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
    # From Python manual:
    # If a class that overrides __eq__() needs to retain the implementation of __hash__()
    # from a parent class, the interpreter must be told this explicitly
    def __hash__(self):
        return super().__hash__()

    def __reduce_ex__(self, proto):
        # this will never run anyway, but the Enum class needs it
        return self.__qualname__

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self._name_) < names.index(other._name_)
        return NotImplemented
