enum34-custom
=============

What
----

Custom Enum classes for the Python 3.4 enum module.


Requirements
------------

* Python 3.4+

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


License
-------

MIT license
