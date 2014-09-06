from enum34_custom import CaseInsensitiveMultiValueEnum, OrderableMixin


class MyInsensitiveMVE(CaseInsensitiveMultiValueEnum):
        one = 1, 'onE', 'OnE'
        two = 2, 'tWo'
        three = 3, 'thrEE'


class OrderableInsensitiveMVE(OrderableMixin, CaseInsensitiveMultiValueEnum):
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
