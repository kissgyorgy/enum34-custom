# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum, EnumMeta, _EnumDict
from functools import total_ordering
from collections import Iterable
import six


__version__ = '0.7.2'
__all__ = ['MultiValueEnum', 'no_overlap', 'StrEnum', 'CaseInsensitiveStrEnum',
           'CaseInsensitiveMultiValueEnum', 'OrderableMixin']


class _MultiValueMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        for member in self.__members__.values():
            values = member._value_
            # make sure we only have tuple values, not single values
            if (not isinstance(values, Iterable) or
                    isinstance(values, six.string_types)):
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                                .format(member._name_, values, type(values)))
            for alias in values:
                # don't touch if already set, so behave like alias
                # described in python documentation
                self._value2member_map_.setdefault(alias, member)


class MultiValueEnum(six.with_metaclass(_MultiValueMeta, Enum)):
    """Enum subclass where a member can be any iterable (except str).
    You can reference a member by any of its element in the associated iterable.
    """


class _CasInsensitiveMultiValueMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            values = member._value_
            if (not isinstance(values, Iterable) or
                    isinstance(values, six.string_types)):
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                                .format(member._name_, values, type(values)))
            for alias in values:
                if isinstance(alias, six.text_type):
                    alias = alias.upper()
                self._value2member_map_.setdefault(alias, member)

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed."""
        if isinstance(value, six.text_type):
            value = value.upper()
        return super(_CasInsensitiveMultiValueMeta, cls).__call__(value)


class CaseInsensitiveMultiValueEnum(
        six.with_metaclass(_CasInsensitiveMultiValueMeta, Enum)):
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
            intersection = set(member._value_) & set(prev_member._value_)
            if intersection:
                duplicates.append((member._name_, prev_member._name_, intersection))
        members.append(member)

    if duplicates:
        alias_details = ', '.join(["{} & {} -> {}".format(alias, name, intersection)
                                  for (alias, name, intersection) in duplicates])
        raise ValueError('common element found in {!r}: {}'
                         .format(multienum, alias_details))
    return multienum


class _CheckTypeDict(_EnumDict):
    def __init__(self, expected_type):
        super(_CheckTypeDict, self).__init__()
        self._expected_type = expected_type

    def __setitem__(self, key, value):
        super(_CheckTypeDict, self).__setitem__(key, value)
        if not isinstance(value, self._expected_type):
            raise TypeError('{} = {!r}, should be {}!'.format(
                            key, value, self._expected_type))


class StrEnum(six.text_type, Enum):
    """Enum subclass which members are also instances of str
    and directly comparable to strings. str type is forced at declaration.
    """
    def __new__(cls, *args):
        for arg in args:
            if not isinstance(arg, six.text_type):
                raise TypeError('Not text %s:' % arg)
        return super(StrEnum, cls).__new__(cls, *args)


class _CaseInsensitiveEnumMeta(EnumMeta):
    def __init__(self, cls, bases, classdict):
        for name, member in self._member_map_.items():
            self._value2member_map_.pop(member._value_)
            member._value_ = member.value.upper()
            # need to update also
            self._value2member_map_[member._value_] = member

    def __call__(cls, value):
        return cls.__new__(cls, value.upper())


class CaseInsensitiveStrEnum(
        six.with_metaclass(_CaseInsensitiveEnumMeta, six.text_type, Enum)):
    def __new__(cls, *args):
        checkargs = []
        for arg in args:
            if isinstance(arg, six.text_type):
                checkargs.append(arg.upper())
            else:
                raise TypeError('Not text %s:' % arg)
        return super(CaseInsensitiveStrEnum, cls).__new__(cls, *checkargs)

    def __eq__(self, other):
        return self.upper() == other.upper()


@total_ordering
class OrderableMixin(object):
    """Mixin for comparable Enums. The order is the definition order
    from smaller to bigger.
    """
    # From Python manual:
    # If a class that overrides __eq__() needs to retain
    # the implementation of __hash__() from a parent class,
    # the interpreter must be told this explicitly
    def __hash__(self):
        return super(OrderableMixin, self).__hash__()

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
