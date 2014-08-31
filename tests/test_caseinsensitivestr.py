from enum34_custom import CaseInsensitiveStrEnum
from pytest import raises


class MyCaseInsensitiveStrEnum(CaseInsensitiveStrEnum):
    one = 'a'
    two = 'b'


def test_members_are_instances_of_builtin_str():
    assert isinstance(MyCaseInsensitiveStrEnum.one, str)


def test_members_are_also_instances_of_StrEnum():
    assert isinstance(MyCaseInsensitiveStrEnum.one, MyCaseInsensitiveStrEnum)


def test_raises_TypeError_with_not_str_type():
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
