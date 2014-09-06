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

   from enum34_custom import MultiValueEnum

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

     >>> from enum34_custom import MultiValueEnum, no_overlap

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

   from enum34_custom import CaseInsensitiveStrEnum
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



.. |travis| image:: https://travis-ci.org/Walkman/enum34-custom.svg?branch=master
   :target: https://travis-ci.org/Walkman/enum34-custom

.. |coveralls| image:: https://coveralls.io/repos/Walkman/enum34-custom/badge.png?branch=master
   :target: https://coveralls.io/r/Walkman/enum34-custom?branch=master

.. |pythons| image:: https://pypip.in/py_versions/enum34-custom/badge.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Supported Python versions

.. |release| image:: https://pypip.in/version/enum34-custom/badge.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Latest Version

.. |license| image:: https://pypip.in/license/enum34-custom/badge.svg
   :target: https://github.com/Walkman/enum34-custom/blob/master/LICENSE
   :alt: MIT License

.. |downloads| image:: https://pypip.in/download/enum34-custom/badge.svg
   :target: https://pypi.python.org/pypi/enum34-custom/
   :alt: Downloads
