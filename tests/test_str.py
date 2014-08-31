from pytest import raises
from enum34_custom import StrEnum


class MyStrEnum(StrEnum):
    one = '1'
    two = '2'


class MyOtherStrEnum(StrEnum):
    one = '1'
    three = '3'
    four = '4'


class MyReverseOrderedStrEnum(StrEnum):
    # >>> '1' < '2'
    # True
    one = '4'
    two = '3'
    three = '2'
    four = '1'


def test_members_are_instances_of_builtin_str():
    assert isinstance(MyStrEnum.one, str)


def test_members_are_also_instances_of_StrEnum():
    assert isinstance(MyStrEnum.one, MyStrEnum)


def test_raises_TypeError_with_not_str_type():
    with raises(TypeError):
        class MyBadTypeStrEnum(StrEnum):
            a = '1'
            b = 2


def test_comparable_to_str():
    assert MyStrEnum.one == '1'


def test_comparable_to_other_Enum_instances():
    assert MyStrEnum.one == MyOtherStrEnum.one \
                         == MyReverseOrderedStrEnum.four == '1'


def test_comparison_will_happen_based_on_str_value():
    assert MyReverseOrderedStrEnum.one > MyReverseOrderedStrEnum.two


def test_members_are_comparable_to_simple_str_instances():
    assert MyReverseOrderedStrEnum.one < 'A'
    assert MyReverseOrderedStrEnum.one <= 'A'
