class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final

    def __str__(self):
        return self.name + ": " + str(self.final)


class FA:
    def __init__(self, file):
        self.states = []
        self.trans = {}

        with open(file, "r") as f:
            states_r = f.readline().split()
            final_states_nr = int(f.readline())
            self.alphabet = f.readline().split()
            for line in f:
                line = line.split()
                if line[2] not in self.trans.keys():
                    self.trans[line[2]] = []
                self.trans[line[2]].append((line[0], line[1]))

        for state in states_r:
            self.states.append(State(state))
            if len(self.states) > len(states_r) - final_states_nr:
                self.states[-1].final = True
