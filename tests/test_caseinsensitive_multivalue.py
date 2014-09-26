# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six import PY2
from enum_custom import CaseInsensitiveMultiValueEnum, OrderableMixin


class MyInsensitiveMVE(CaseInsensitiveMultiValueEnum):
        one = 1, 'onE', 'OnE'
        two = 2, 'tWo'
        three = 3, 'thrEE'


class OrderableInsensitiveMVE(OrderableMixin, CaseInsensitiveMultiValueEnum):
    # In Python 2 classes don't have definition order,
    # you have to specify it manually
    if PY2:
        __order__ = 'one two three'
    one = 'e', 'f'
    two = 'c', 'd'
    three = 'a', 'b'


def test_uppercase():
    assert MyInsensitiveMVE('ONE') == MyInsensitiveMVE.one
    assert MyInsensitiveMVE('oNE') == MyInsensitiveMVE.one
    assert MyInsensitiveMVE('one') == MyInsensitiveMVE.one


def test_not_str_values_are_untouched():
    assert MyInsensitiveMVE(2).value == (2, 'tWo')
    assert MyInsensitiveMVE(2) == MyInsensitiveMVE.two


def test_orderable():
    assert ('e', 'f') > ('c', 'd')
    assert ('c', 'd') > ('a', 'b')

    assert OrderableInsensitiveMVE.one < OrderableInsensitiveMVE.two
    assert OrderableInsensitiveMVE.two < OrderableInsensitiveMVE.three
