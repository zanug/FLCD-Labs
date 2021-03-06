class Grammar:
    def __init__(self, file):
        self.productions = {}

        with open(file, "r") as f:
            self.non_terminals = set(f.readline().split())
            self.terminals = set(f.readline().split())

            first = True
            for line in f:
                line = line.split(":")
                if line[0] in self.non_terminals:
                    results = set(line[1].split("|"))
                    self.productions[line[0]] = []
                    if first:
                        self.starting_symbol = line[0]
                        first = False
                    for res in results:
                        res = res.split()
                        good = True
                        for r in res:
                            if r not in self.terminals and r not in self.non_terminals:
                                good = False
                        if good:
                            self.productions[line[0]].append(res)

    def get_terminals(self):
        return self.terminals

    def get_non_terminals(self):
        return self.non_terminals

    def get_all_symbols(self):
        return list(self.get_non_terminals()) + list(self.get_terminals())

    def get_starting_symbol(self):
        return self.starting_symbol

    def get_productions(self):
        return self.productions

    def get_productions_for(self, non_terminal):
        return self.productions[non_terminal]

