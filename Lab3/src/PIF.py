class PIFEntry:
    def __init__(self, token, st_pos):
        self.token = token
        self.st_pos = st_pos

    def __str__(self):
        return "token: {}, st_entry: {}".format(self.token, self.st_pos)


class PIF:
    def __init__(self):
        self.table = []

    def append(self, e):
        self.table.append(e)

    def __str__(self):
        string = "PIF Table: " \
                 "\n\n{:<10} {:<5}\n".format("Token", "ST Entry")

        for e in self.table:
            string += "\n{:<10} {:<5}".format(e.token, e.st_pos)

        return string