import copy
from queue import Queue

import numpy as np


class Production:
    def __init__(self, left_hand_side, right_hand_side, dot=0):
        self.left_hand_side = left_hand_side  # Non-Terminal
        self.right_hand_side = right_hand_side  # List of Right Hand Side Items (Strings)
        self.dot = dot  # Dot position

    # Example: A → •aA ==> lhs: A; rhs: [a, A]; dot: 0

    def __eq__(self, other):
        if self.dot == other.dot and \
                self.left_hand_side == other.left_hand_side and \
                self.right_hand_side == other.right_hand_side:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.left_hand_side)

    def __str__(self):
        return "Production: {} -> {}; dot: {}".format(self.left_hand_side, self.right_hand_side, self.dot)

    def __repr__(self):
        return "\nProduction: {} -> {}; dot: {}".format(self.left_hand_side, self.right_hand_side, self.dot)


class State:
    def __init__(self, set):
        self.set = set

    def add(self, e):
        self.set.add(e)

    def __str__(self):
        return "State: " + str(self.set)

    def __repr__(self):
        return "State: " + str(self.set) + "\n"

    def __eq__(self, other):
        if len(self.set) != len(other.set):
            return False
        if len(self.set.intersection(other.set)) == len(self.set):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1


class ParsingTable:
    def __init__(self, states, terminals, non_terminals):
        self.states = states
        self.nr_rows = len(states)
        self.nr_cols = len(terminals) + len(non_terminals)
        self.goto = np.array([[-1 for _ in range(self.nr_cols)] for _ in range(self.nr_rows)])
        self.action = ["" for _ in range(self.nr_rows)]
        self.symbols = list(terminals) + list(non_terminals)

    def __str__(self):
        string = "Parsing Table:\n"
        string += "{:<4} {:<15} {:<6}\n".format("nr", "action", "goto")
        string += "{:<4} {:<15}".format("", "")
        for i in range(self.nr_cols):
            string += "{:>4}".format(self.symbols[i])
        string += "\n\n"
        for i in range(self.nr_rows):
            string += str("{:<4} {:<15}".format(i, self.action[i]))
            for j in range(self.nr_cols):
                string += "{:>4}".format(self.goto[i][j])
            string += "\n"

        return string


class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammar.productions['S\''] = [[grammar.get_starting_symbol()]]
        self.grammar.starting_symbol = "S'"
        # print(grammar.productions)

        self.states = []

    def closure(self, productions):
        closure = set(productions)

        queue = Queue()

        for production in productions:
            queue.put(production)

        while not queue.empty():
            production = queue.get()
            # print(production)
            if production.dot < len(production.right_hand_side):
                lhs = production.right_hand_side[production.dot]
                # print("lhs:", lhs)
                if lhs in self.grammar.non_terminals:
                    for rhs in self.grammar.productions[lhs]:
                        prod = Production(lhs, rhs)
                        # print("-----", prod)
                        if prod not in closure:
                            closure.add(prod)
                            queue.put(prod)
        return closure

    def goto(self, state, elem):
        new_state = []
        for production in state:
            if production.dot < len(production.right_hand_side) and production.right_hand_side[production.dot] == elem:
                production.dot += 1
                new_state.append(production)
        return self.closure(new_state)

    def get_states(self):
        c_state = self.closure(
            [Production(self.grammar.starting_symbol,
                        self.grammar.productions[self.grammar.starting_symbol][0])])
        states = [State(c_state)]
        c_state_idx = -1

        edges = {}

        while c_state_idx < len(states) - 1:
            c_state_idx += 1

            state = states[c_state_idx]

            for symbol in self.grammar.get_all_symbols():
                goto_productions = []
                for production in state.set:
                    if production.dot < len(production.right_hand_side) and \
                            production.right_hand_side[production.dot] == symbol:
                        goto_productions.append(copy.deepcopy(production))  # !!!!!!!!!! DEEPCOPY NEEDED !!!!!!!!!!!!
                    if len(goto_productions):
                        goto = self.goto(goto_productions, symbol)
                        if len(goto) != 0:
                            if State(goto) not in states:
                                # print(states)
                                # print("goto:", goto, "\nsymbol:", symbol)
                                states.append(State(goto))
                                edges[(c_state_idx, symbol)] = len(states) - 1
                                # TODO: CHECK 4 CONFLICTS
                            else:
                                edges[(c_state_idx, symbol)] = states.index(State(goto))

        return states, edges

    def create_parsing_table(self):
        states, edges = self.get_states()
        parsing_table = ParsingTable(states, self.grammar.terminals, self.grammar.non_terminals)
        for i in range(parsing_table.nr_rows):
            for j in range(parsing_table.nr_cols):
                if (i, parsing_table.symbols[j]) in edges.keys():
                    parsing_table.goto[i][j] = edges[(i, parsing_table.symbols[j])]
                    parsing_table.action[i] = "s"

            if parsing_table.action[i] == "":
                state = parsing_table.states[i]
                err = True
                for production in state.set:
                    if production.dot == len(production.right_hand_side):
                        if production.left_hand_side == self.grammar.starting_symbol:
                            parsing_table.action[i] = "acc"
                            err = False
                            break
                        else:
                            idx = self.grammar.productions[production.left_hand_side].index(production.right_hand_side)
                            # reduce, key in grammar.productions, index in list of productions 4 key
                            #                             ^
                            parsing_table.action[i] = "r {} {}".format(production.left_hand_side, idx)
                            err = False
                            break
                if err:
                    parsing_table.action[i] = "err"
        return parsing_table

    def parse(self, string):
        parsing_table = self.create_parsing_table()
        work_stack = ["$", 0]  # Starting state is always the first in this implementation
        input_stack = string.split() + ["$"]
        output = []
        # print("input stack:", input_stack)
        # print("work stack:", work_stack)
        # c_symbol = input_stack[0]
        # c_symbol_idx = parsing_table.symbols.index(c_symbol)

        while True:
            c_state_idx = work_stack[-1]
            if parsing_table.action[c_state_idx] == "acc":
                break
            elif parsing_table.action[c_state_idx] == "s":
                c_symbol = input_stack[0]
                c_symbol_idx = parsing_table.symbols.index(c_symbol)
                if parsing_table.goto[c_state_idx][c_symbol_idx] != -1:
                    work_stack.append(input_stack.pop(0))
                    c_state_idx = parsing_table.goto[c_state_idx][c_symbol_idx]
                    work_stack.append(c_state_idx)

            elif parsing_table.action[c_state_idx][0] == "r":
                r, key, idx = parsing_table.action[c_state_idx].split()
                idx = int(idx)
                c_production = Production(key, self.grammar.productions[key][idx])
                # print("reduce with production:", c_production)
                work_stack = work_stack[:(len(work_stack) - len(c_production.right_hand_side) * 2)]
                c_state_idx = work_stack[-1]
                work_stack.append(c_production.left_hand_side)
                work_stack.append(
                    parsing_table.goto[c_state_idx][parsing_table.symbols.index(c_production.left_hand_side)])
                output.append(c_production)
            else:
                print("ERROR")
                break

            # print("input stack:", input_stack)
            # print("work stack:", work_stack)
            # print("output:", output)

        return output
