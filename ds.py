class OneIndexedList(list):
    """
    OneIndexedList start index from 1 not 0
    just for the convenience
    """

    def __getitem__(self, index):
        return list.__getitem__(self, index-1)
