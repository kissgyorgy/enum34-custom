import pickle
from pytest import raises, raises_regexp
from enum34_custom import MultiValueEnum, OrderableMixin, no_overlap


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
    # because it's an instance of the class.
    assert MyMultiValueEnum(2) != (2, 'two')
    assert MyMultiValueEnum(2).value == (2, 'two')


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


def test_lookup_like_a_dict_is_the_same_as_call():
    assert MyMultiValueEnum['one'] == MyMultiValueEnum.one == MyMultiValueEnum(1)


class TestAcceptAnyIterable:
    def test_accept_set(self):
        class MySetMVE(MultiValueEnum):
            A = set('abcde')
            B = set('fghjk')

        assert MySetMVE.A.value == {'a', 'b', 'c', 'd', 'e'}
        assert MySetMVE('h') == MySetMVE.B

    def test_accept_list(self):
        class MyListMVE(MultiValueEnum):
            A = [n for n in range(5)]
            B = list('abcde')

        assert MyListMVE.A.value == [0, 1, 2, 3, 4]
        assert MyListMVE('e') == MyListMVE.B

    def test_accept_even_generators(self):
        class MyGenMVE(MultiValueEnum):
            A = range(5)
            # generator expressions!
            B = (n for n in (5, 6, 7, 8, 9))
            C = (s for s in 'abcde')

        assert MyGenMVE(4) == MyGenMVE.A
        assert MyGenMVE(5) == MyGenMVE.B
        assert MyGenMVE('a') == MyGenMVE.C
        assert MyGenMVE.A.value == range(5)

    def test_generators_are_immediatly_exhausted(self):
        class MyExhGenMVE(MultiValueEnum):
            A = (n for n in (0, 1, 2, 3, 4))
            B = (n for n in (5, 6, 7, 8, 9))

        # exhausted generator at class instantiation!
        assert list(MyExhGenMVE.A.value) == []

        # you can still look up!
        assert MyExhGenMVE(0) == MyExhGenMVE.A
        assert MyExhGenMVE(5) == MyExhGenMVE.B

        # as many time as you want
        assert MyExhGenMVE(5) == MyExhGenMVE.B
        assert MyExhGenMVE(5) == MyExhGenMVE.B

    def test_dict_keys_will_be_looked_up(self):
        class MyDictMVE(MultiValueEnum):
            A = dict(a=1, b=2, c=3)
            B = {4: 'd', 5: 'e', 6: 'f'}

        assert MyDictMVE('a') == MyDictMVE.A
        assert MyDictMVE(4) == MyDictMVE.B

        with raises(ValueError):
            # no such key in either A or B
            MyDictMVE(2)

        with raises(ValueError):
            MyDictMVE('f')

    def test_except_for_str(self):
        with raises(TypeError):
            class MyBadStrMVE(MultiValueEnum):
                A = 'abcde'
                B = 'fghij'

    def test_make_it_a_list(self):
        class MyGoodStrMVE(MultiValueEnum):
            A = list('abcde')
            B = list('fghij')

        assert MyGoodStrMVE('a') == MyGoodStrMVE.A
        assert MyGoodStrMVE('f') == MyGoodStrMVE.B


class TestReprShowsTypeDefinedInDeclaration:
    def test_generator(self):
        class MyGenMVE(MultiValueEnum):
            A = range(5)
            # generator expressions!
            B = (n for n in (5, 6, 7, 8, 9))
            C = (s for s in 'abcde')

        assert repr(MyGenMVE.A) == '<MyGenMVE.A: range(0, 5)>'
        assert '<generator object <genexpr> at' in repr(MyGenMVE.B)
        assert '<generator object <genexpr> at' in repr(MyGenMVE.C)

    def test_set(self):
        class MySetMVE(MultiValueEnum):
            A = set((1, 2, 3, 4, 5))
            # generator expressions!
            B = set((5, 6, 7, 8, 9))
            C = set('abcde')

        repr_a = repr(MySetMVE.A)
        # set elements are unorderable, never fixed, so have to test this way
        assert all(s in repr_a for s in
                   ('<MySetMVE.A: {', "1" , "2", "3", "4", "5", '}'))

        repr_c = repr(MySetMVE.C)
        assert all(s in repr_c for s in
                   ('<MySetMVE.C: {', "'a'" , "'b'", "'c'", "'d'", "'e'", '}'))


class TestOverlappingBehavior:
    def test_overlapping_elements_behave_as_aliases(self):
        class MyOverLappingMVE(MultiValueEnum):
            A = (0, 1, 2, 3, 4)
            B = (4, 5, 6, 7, 8)

        # 4 is the overlapping element
        assert MyOverLappingMVE(4) == MyOverLappingMVE.A
        assert MyOverLappingMVE(5) == MyOverLappingMVE.B

    def test_overlapping_generator(self):
        class MyOverLappingGenMVE(MultiValueEnum):
            A = range(5)
            B = (n for n in (4, 5, 6, 7, 8))

        assert list(MyOverLappingGenMVE.A.value) == [0, 1, 2, 3, 4]

        # 4 is the overlapping element
        assert MyOverLappingGenMVE(4) == MyOverLappingGenMVE.A
        assert MyOverLappingGenMVE(5) == MyOverLappingGenMVE.B


class TestNoOverapping:
    def test_when_decorating_non_overlapping_enum_nothing_happens(self):
        @no_overlap
        class MyNonOverlappingListMVE(MultiValueEnum):
            A = (1, 2, 3)
            B = (4, 5, 6)

        assert MyNonOverlappingListMVE.A.value == (1, 2, 3)
        assert MyNonOverlappingListMVE(5) == MyNonOverlappingListMVE.B

    def test_decorating_tuple(self):
        error_message = r"common element found in "\
                        r"<enum 'MyOverlappingListMVE'>: B & A -> \{3\}"
        with raises_regexp(ValueError, error_message):
            @no_overlap
            class MyOverlappingListMVE(MultiValueEnum):
                A = (1, 2, 3)
                B = (3, 4, 5)

    def test_decorating_generator(self):
        error_message = r"common element found in "\
                        r"<enum 'MyOverlappingGenMVE'>: "\
                        r"B & A -> \{0, 1, 2, 3, 4\}"
        with raises_regexp(ValueError, error_message):
            @no_overlap
            class MyOverlappingGenMVE(MultiValueEnum):
                A = range(5)
                B = range(10)


class TestAliases:
    def test_alias_should_pick_first_value(self):
        class MyAliasedMVE(MultiValueEnum):
            one = 1, 'one', 'One'
            two = 2, 'two'
            three = 3, 'three'
            alias_to_one = 1, 'one', 'One'

        assert MyAliasedMVE.alias_to_one is MyAliasedMVE.one
        assert MyAliasedMVE('one') is MyAliasedMVE.one
        assert MyAliasedMVE(1) is MyAliasedMVE.one

    def test_defining_alias_with_referencing_previous(self):
        class MyAliasedMVE(MultiValueEnum):
            one = 1, 'one', 'One'
            two = 2, 'two'
            three = 3, 'three'
            alias_to_one = one

        assert MyAliasedMVE.alias_to_one is MyAliasedMVE.one
        assert MyAliasedMVE('one') is MyAliasedMVE.one
        assert MyAliasedMVE(1) is MyAliasedMVE.one


def test_idempotency():
    class MyIdempotentMVE(MultiValueEnum):
        one = 1, 2
        two = 3, 4

    assert MyIdempotentMVE(MyIdempotentMVE.one) is MyIdempotentMVE.one


def test_lookup_by_original_value():
    class MyOriginalMVE(MultiValueEnum):
        one = 1, 2
        two = {3, 4}

    assert MyOriginalMVE((1, 2)) is MyOriginalMVE.one
    assert MyOriginalMVE({3, 4}) is MyOriginalMVE.two


def test_pickable():
    # the class doesn't play nicely when defined inside other namespace
    # http://stackoverflow.com/a/4677063/720077
    dumped = pickle.dumps(MyOrderableMultiValueEnum.one)
    assert pickle.loads(dumped) is MyOrderableMultiValueEnum.one


def test_hashable():
    assert hash(MyOrderableMultiValueEnum.one) == hash(MyOrderableMultiValueEnum(1))


def test_aliases_doesnt_get_listed():
    class MyAliasedMVE(MultiValueEnum):
        one = 1, 'one', 'One'
        two = 2, 'two'
        three = 3, 'three'
        alias_to_one = 1, 'one', 'One'

    assert list(MyAliasedMVE) == [MyAliasedMVE.one, MyAliasedMVE.two, MyAliasedMVE.three]
