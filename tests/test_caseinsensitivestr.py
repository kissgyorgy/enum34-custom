# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six import text_type
from pytest import raises
from enum_custom import CaseInsensitiveStrEnum


class MyCaseInsensitiveStrEnum(CaseInsensitiveStrEnum):
    one = 'a'
    two = 'b'


def test_members_are_instances_of_text_type():
    assert isinstance(MyCaseInsensitiveStrEnum.one, text_type)


def test_members_are_also_instances_of_StrEnum():
    assert isinstance(MyCaseInsensitiveStrEnum.one, MyCaseInsensitiveStrEnum)


def test_raises_TypeError_with_not_text_type():
    with raises(TypeError):
        class MyBadCaseInsensitiveStrEnum(CaseInsensitiveStrEnum):
            a = '1'
            b = 2


def test_comparable_to_str():
    assert MyCaseInsensitiveStrEnum.one == 'a'
    assert MyCaseInsensitiveStrEnum.one == 'A'


def test_comparison_will_happen_based_on_str_value():
    assert MyCaseInsensitiveStrEnum.one < MyCaseInsensitiveStrEnum.two


def test_case_insensitivity():
    assert MyCaseInsensitiveStrEnum('a') == 'A'
    assert MyCaseInsensitiveStrEnum('A') == 'a'
