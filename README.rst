enum34-custom
=============

|travis| |coveralls| |release| |downloads| |pythons| |license|

What
----

Custom Enum classes for the Python 3.4 enum module.


Install
-------

.. code-block:: bash

   $ pip install enum34-custom


Usage
-----

MultiValueEnum
^^^^^^^^^^^^^^

Enum subclass where a member can be any iterable (even a generator, except str).
You can reference a member by any of its element in the associated iterable.
It might be usable for e.g. Equivalence Class Partitioning (ECP/EC testing).


.. code-block:: python

   from enum_custom import MultiValueEnum

   class Suit(MultiValueEnum):
       CLUBS =    '♣', 'c', 'C'
       DIAMONDS = '♦', 'd', 'D'
       HEARTS =   '♥', 'h', 'H'
       SPADES =   '♠', 's', 'S'

   >>> print(Suit.CLUBS)
   Suit.CLUBS

   >>> Suit.CLUBS
   <Suit.CLUBS: ('♣', 'c', 'C')>

   >>> Suit('c')
   <Suit.CLUBS: ('♣', 'c', 'C')>

   >>> Suit('c') is Suit('C') is Suit('♣') is Suit.CLUBS
   True

   >>> import pickle
   >>> pickle.loads(pickle.dumps(Suit('c'))) is Suit('♣')
   True

   >>> Suit('L')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/walkman/Projects/enum34-custom/enum34_custom.py", line 19, in __call__
       return super().__call__(suit)
     File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/enum.py", line 222, in __call__
       return cls.__new__(cls, value)
     File "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/enum.py", line 457, in __new__
       raise ValueError("%s is not a valid %s" % (value, cls.__name__))
   ValueError: L is not a valid Suit

   >>> list(Suit)
   [<Suit.CLUBS: ('♣', 'c', 'C')>,
    <Suit.DIAMONDS: ('♦', 'd', 'D')>,
    <Suit.HEARTS: ('♥', 'h', 'H')>,
    <Suit.SPADES: ('♠', 's', 'S')>]


.. warning::

   You need to keep a couple of things in mind when using MultiValueEnum:


* Generators will immediately be exhausted at class creation time!
* To conform to the standard library behavior, overlapping iterables are
  considered aliases, and works the same way as in stdlib
  (lookup will match the first declared element):

  .. code-block:: python

     >>> class MyOverLappingMVE(MultiValueEnum):
     ...     A = (0, 1, 2, 3, 4)
     ...     B = (4, 5, 6, 7, 8)
     >>> MyOverLappingMVE(4)
     <MyOverLappingMVE.A: (0, 1, 2, 3, 4)>

  If you want to make sure, no overlapping elements are present between members,
  you can use the no_overlap decorator:

  .. code-block:: python

     >>> from enum_custom import MultiValueEnum, no_overlap

     >>> @no_overlap
     ... class NoOverLappingEnum(MultiValueEnum):
     ...     A = (1, 2, 3)
     ...     B = (3, 4, 5)
     ...
     /Users/walkman/Projects/enum34-custom/enum34_custom.py in no_overlap(multienum)
          55                                   (alias, name, intersection) in duplicates])
          56         raise ValueError('common element found in {!r}: {}'
     ---> 57                          .format(multienum, alias_details))
          58     return multienum
          59

     ValueError: common element found in <enum 'NoOverLappingEnum'>: B & A -> {3}

* Beware with storing lots of data, every value will stored twice
  (MultiValueEnum stores values internally in a set for faster lookups)
* If you declare a dict as a value, keys will be looked up (as expected)


CaseInsensitiveMultiValueEnum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This works the same way as MultiValueEnum except if a member's value contains
a str, those will be compared in a case-insensitive member.

Consider the following example:

.. code-block:: python

   class SimpleMultiValueEnum(MultiValueEnum):
       one = 1, 'one'
       two = 2, 'two'

   >>> SimpleMultiValueEnum('One')
   /usr/local/Cellar/python3/3.4.1_1/Frameworks/Python.framework/Versions/3.4/lib/python3.4/enum.py in __new__(cls, value)
       455                 if member.value == value:
       456                     return member
   --> 457         raise ValueError("%s is not a valid %s" % (value, cls.__name__))
       458
       459     def __repr__(self):

   ValueError: One is not a valid SimpleMultiValueEnum

While:

.. code-block:: python

   class CaseInsensitiveMVE(CaseInsensitiveMultiValueEnum):
       one = 1, 'one'
       two = 2, 'two'

   >>> CaseInsensitiveMVE('One')
   <CaseInsensitiveMVE.one: (1, 'one')>


StrEnum
^^^^^^^

Members of this enum are also instances of str and directly comparable to strings.
str type is forced at declaration. Works the same way as described in Python
Enum documentation, except for checking type.

.. warning::

   It's not possible to use StrEnum with OrderableMixin, because the members of
   StrEnum are also instances of str and ordering members will happen beased on
   str ordering (e.g. '1' < '2', 'A' < 'B', etc.)
   If you want ordering by declaration, use OrderableMixin without typed
   subclass.


CaseInsensitiveStrEnum
^^^^^^^^^^^^^^^^^^^^^^

Same as StrEnum, but members stored as uppercase, and comparing to them is
case insensitive also:

.. code-block:: python

   from enum_custom import CaseInsensitiveStrEnum
   class MyCaseInsensitiveStrEnum(CaseInsensitiveStrEnum):
       one = 'a'
       two = 'b'

   >>> MyCaseInsensitiveStrEnum('a') == 'A'
   True
   >>> MyCaseInsensitiveStrEnum.one == 'a'
   True


Testing
-------

.. code-block:: bash

   $ python setup.py test


Or install package in development mode and test with py.test::

   $ pip install -e .
   $ py.test


Differences between Python 2 and 3
----------------------------------

There are differences in how Python 2 and 3 creates classes, there are a couple of
things that doesn't work very well on 2, which you should be aware:

- xrange(5) != xrange(5)
  This is the opposit in Python 3, because range(5) == range(5), however you can use
  range(5) == range(5) in Python 2 in this case.
- Python 2 have no definition order of members. This means you *have to* manually define
  __order__ attribute to be able to compare members by definition order (e.g. with
  OrderableMixin). See the details in `enum34 package dokumentation`_:
- str vs unicode: This library doesn't mix and match str types either in Python2
  it uses unicode in Python2 and str in Python3 and also enforces the type in
  StrEnum, CaseInsensitiveStrEnum and ckeck for text type only in
  CaseInsensitiveMultiValueEnum. (So if you pass str in Python2, it will not be case
  insensitive!)
- Python 2 leaks variables from list comprehensions, so if you define your class
  like this:
- On pypy you always have to set __order__ because if you use different types, because
  it would sort the member values, but can't compare set to other type.

  .. code-block:: python

     class MyList(MultiValueEnum):
         A = [n for n in range(5)]

  MyList will have 'MyList.n' also!!!


Changes
-------

v0.7.0
^^^^^^

- Python 2.7 support
- Renamed module to enum_custom for consistency (enum34 package is called enum also).



.. _enum34 package dokumentation: https://pypi.python.org/pypi/enum34

.. |travis| image:: https://travis-ci.org/kissgyorgy/enum34-custom.svg?branch=master
   :target: https://travis-ci.org/kissgyorgy/enum34-custom

.. |coveralls| image:: https://coveralls.io/repos/kissgyorgy/enum34-custom/badge.png?branch=master
   :target: https://coveralls.io/r/kissgyorgy/enum34-custom?branch=master

.. |pythons| image:: https://img.shields.io/pypi/pyversions/enum34-custom.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Supported Python versions

.. |release| image:: https://img.shields.io/pypi/v/enum34-custom.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Latest Version

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/kissgyorgy/enum34-custom/blob/master/LICENSE
   :alt: MIT License

.. |downloads| image:: https://img.shields.io/pypi/dm/enum34-custom.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Downloads
