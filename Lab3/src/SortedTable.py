class STEntry:
    def __init__(self, data, next):
        self.data = data
        self.next = next

    def __str__(self):
        return "Data: {}, Next: {}".format(self.data, self.next)


class SortedTable:
    def __init__(self):
        self.__start_idx = -1
        self.__table = []

    def __str__(self):
        string = "Symbol Table: " \
                 "\nStart index: {}" \
                 "\n\n{:<5} {:<15} {:<5}\n".format(self.__start_idx, "Idx", "Value", "Next")

        for i in range(len(self.__table)):
            string += "\n{:<5} {:<15} {:<5}".format(i, self.__table[i].data, self.__table[i].next)
        return string

    def next(self, cidx):
        return self.__table[cidx].next

    def append(self, data):
        prev = -1
        idx = self.__start_idx

        while idx != -1 and self.__table[idx].data < data:
            prev = idx
            idx = self.next(idx)

        if idx != -1 and self.__table[idx].data == data:
            return

        self.__table.append(STEntry(data, idx))

        if prev == -1:
            self.__start_idx = len(self.__table) - 1
        else:
            self.__table[prev].next = len(self.__table) - 1

    def getById(self, idx):
        return self.__table[idx]

    def search(self, data):
        idx = self.__start_idx

        while idx != -1 and self.__table[idx].data < data:
            idx = self.next(idx)

        if self.__table[idx].data == data:
            return idx
        return -1
