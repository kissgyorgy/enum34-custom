enum34-custom
=============

What
----

Custom Enum classes for the Python 3 enum module.

Requirements
------------

* Python 3.4+

Usage
-----

.. code-block:: python

    from enum34_custom import MultiValueEnum

    class Suit(MultiValueEnum):
        CLUBS =    '♣', 'c', 'C'
        DIAMONDS = '♦', 'd', 'D'
        HEARTS =   '♥', 'h', 'H'
        SPADES =   '♠', 's', 'S'


>>> print(Suit.CLUBS)
♣

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


Test
----

I'm lazy :D


More to come
------------

See above :)
