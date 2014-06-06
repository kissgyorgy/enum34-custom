from enum import Enum, EnumMeta


class _MultiMeta(EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        enum_class = super(_MultiMeta, metacls).__new__(metacls, cls, bases, classdict)
        # make sure we only have tuple values, not single values
        for member in enum_class.__members__.values():
            if not isinstance(member.value, tuple):
                raise ValueError('{!r}, should be tuple'.format(member.value))
        return enum_class

    def __call__(cls, suit):
        """Return the appropriate instance with any of the values listed."""
        for member in cls:
            if suit in member.value:
                return member
        # raise ValueError otherwise
        return super().__call__(suit)


class MultiValueEnum(Enum, metaclass=_MultiMeta):
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self.name) < names.index(other.name)
        return NotImplemented

    def __str__(self):
        return self.value[0]
