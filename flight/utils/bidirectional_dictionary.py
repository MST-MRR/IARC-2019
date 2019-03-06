"""A dictionary and can be searched by key or by value."""

class BidirectionalDictionary:
    """A dictionary that built off of a list that can be searched with either
    the key or the value.

    Attributes
    ----------
    _dict
        The internal dictionary.
    """

    def __init__(self, alist):
        """Constructs a bidirectional dictionary from a list.

        Parameters
        ----------
        alist : list
            The list to turn into a dictionary.
        """
        if not isinstance(alist, list):
            raise TypeError

        if not alist:
            raise ValueError

        self._dict = {}

        for index, item in zip(range(0, len(alist)), alist):
            self._dict[index] = item
            self._dict[item] = index

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value
