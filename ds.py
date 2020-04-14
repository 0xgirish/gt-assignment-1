# OneIndexedList start index from 1 not 0
# just for the convenience
class  OneIndexedList(list):
    def __getitem__(self, index):
        return list.__getitem__(self, index-1)
