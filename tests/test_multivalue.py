from pytest import raises
from enum34_custom import MultiValueEnum, OrderableMixin


class MyMultiValueEnum(MultiValueEnum):
        one = 1, 'one', 'One'
        two = 2, 'two'
        three = 3, 'three'


class MyOrderableMultiValueEnum(OrderableMixin, MultiValueEnum):
    one = 1, 'one', 'One'
    two = 2, 'two'
    three = 3, 'three'


def test_equality():
    assert MyMultiValueEnum(2) == MyMultiValueEnum.two == MyMultiValueEnum('two')
    assert MyMultiValueEnum.one.value == (1, 'one', 'One')
    assert MyMultiValueEnum(2).value == MyOrderableMultiValueEnum.two.value


def test_not_comparable_with_other_types():
    assert MyMultiValueEnum(2) != MyOrderableMultiValueEnum(2)
    assert MyMultiValueEnum(2) != (2, 'two')


def test_identity():
    assert isinstance(MyMultiValueEnum(2), MultiValueEnum)
    assert isinstance(MyOrderableMultiValueEnum(2), MyOrderableMultiValueEnum)
    assert MyMultiValueEnum(3) is MyMultiValueEnum.three
    assert id(MyMultiValueEnum('two')) == id(MyMultiValueEnum(2))
    assert id(MyMultiValueEnum('two')) != MyMultiValueEnum(3)
    assert MyMultiValueEnum('three') != (3, 'three')
    assert (MyMultiValueEnum(3) is (3, 'three')) is False


def test_not_orderable():
    with raises(TypeError):
        assert MyMultiValueEnum(2) < MyMultiValueEnum(3)

    with raises(TypeError):
        assert MyMultiValueEnum(2) < MyOrderableMultiValueEnum(3)

    with raises(TypeError):
        assert MyOrderableMultiValueEnum(2) < MyMultiValueEnum(3)


def test_not_tuple_members_raises_TypeError():
    # Explicit is better than implicit. Do this rather than implicitly
    # handle single values to avoid confusion or typos
    with raises(TypeError):
        class MyBadMultiValueEnum(MultiValueEnum):
            one = 1, 'one'
            two = 2

    with raises(TypeError):
        class MyBadMultiValueEnum2(MultiValueEnum):
            one = [1, 'one']
            two = [2, 'two']


def test_incorrect_value_raises_ValueError():
    with raises(ValueError):
        MyMultiValueEnum('B')

    with raises(ValueError):
        # case is different
        MyMultiValueEnum('ONE')


def test_list():
    assert list(MyMultiValueEnum) == [
        MyMultiValueEnum.one,
        MyMultiValueEnum.two,
        MyMultiValueEnum.three,
    ]


def test_list_with_OrderableMixin():
    assert list(MyOrderableMultiValueEnum) == [
        MyOrderableMultiValueEnum.one,
        MyOrderableMultiValueEnum.two,
        MyOrderableMultiValueEnum.three,
    ]


def test_orderable_with_mixin():
    assert MyOrderableMultiValueEnum(1) < MyOrderableMultiValueEnum(2)
    assert MyOrderableMultiValueEnum.one < MyOrderableMultiValueEnum.two
    assert MyOrderableMultiValueEnum(1) < MyOrderableMultiValueEnum(3)
    assert MyOrderableMultiValueEnum(2) < MyOrderableMultiValueEnum(3)

    assert MyOrderableMultiValueEnum(1) <= MyOrderableMultiValueEnum(2)
    assert MyOrderableMultiValueEnum(1) <= MyOrderableMultiValueEnum(3)
    assert MyOrderableMultiValueEnum(2) <= MyOrderableMultiValueEnum(3)
    assert MyOrderableMultiValueEnum.two <= MyOrderableMultiValueEnum.three

    assert MyOrderableMultiValueEnum(3) > MyOrderableMultiValueEnum(1)
    assert MyOrderableMultiValueEnum('three') > MyOrderableMultiValueEnum('two')
    assert MyOrderableMultiValueEnum(3) > MyOrderableMultiValueEnum('One')
    assert MyOrderableMultiValueEnum.three > MyOrderableMultiValueEnum.one

    assert MyOrderableMultiValueEnum(3) >= MyOrderableMultiValueEnum(1)
    assert MyOrderableMultiValueEnum('three') >= MyOrderableMultiValueEnum('two')
    assert MyOrderableMultiValueEnum(3) >= MyOrderableMultiValueEnum('One')
    assert MyOrderableMultiValueEnum.three >= MyOrderableMultiValueEnum.one
