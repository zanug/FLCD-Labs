from queue import Queue


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
            final_states = f.readline().split()
            self.alphabet = f.readline().split()

            for state in states_r:
                self.states.append(State(state))
                if final_states[len(self.states) - 1] == "1":
                    self.states[-1].final = True

            for line in f:
                line = line.split()
                if (line[0], line[2]) not in self.trans.keys():
                    self.trans[(line[0], line[2])] = []
                self.trans[(line[0], line[2])].append(line[1])

    def check_sequence(self, sequence):
        queue = Queue()
        queue.put((self.states[0].name, 0))

        while not queue.empty():
            c_step = queue.get()
            c_node = c_step[0]
            c_pos_sequence = c_step[1]


            if (c_node, sequence[c_pos_sequence]) in self.trans.keys():
                if c_pos_sequence + 1 == len(sequence):
                    return True
                for node in self.trans[(c_node, sequence[c_pos_sequence])]:
                    queue.put((node, c_pos_sequence + 1))

        return False

    def get_all_states(self):
        res = []
        for s in self.states:
            res.append(s.name)
        return res

    def get_init_state(self):
        return self.states[0].name

    def get_final_states(self):
        res = []
        for s in self.states:
            if s.final:
                res.append(s.name)
        return res

    def get_alphabet(self):
        return self.alphabet

    def get_transitions(self):
        return self.trans

    def dfa(self):
        for k in self.trans.keys():
            if len(self.trans[k]) > 1:
                return False
        return True
