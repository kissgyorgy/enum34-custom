enum34-custom |travis| |coveralls| |release| |downloads| |pythons| |license|
============================================================================

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


StrEnum
^^^^^^^

.. warning::

   It's not possible to use StrEnum with OrderableMixin, because the members of
   StrEnum are also instances of str and ordering members will happen beased on
   str ordering (e.g. '1' < '2', 'A' < 'B', etc.)
   If you want ordering by declaration, use OrderableMixin without typed
   subclass.


FAQ
---
**Q:** Why can I only declare tuples and not any iterable in MultiValueEnum?

**A:** This way class definition looks clean. By default you don't have to put paranthesis
if you define a tuple, but you need to if you want to define a list.
Tuples are simple, declaration should be minimal.


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
