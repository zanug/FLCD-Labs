from Lab4.src.FA import FA


def menu():
    while True:
        print("\n1: Show all states")
        print("2: Show initial state")
        print("3: Show final states")
        print("4: Show alphabet")
        print("5: Show transitions")
        print("6: Is it DFA?")
        print("t: Test a sequence")
        print("x: exit")
        com = input("->")
        if com == "x":
            break
        elif com == "1":
            print(fa.get_all_states())
        elif com == "2":
            print(fa.get_init_state())
        elif com == "3":
            print(fa.get_final_states())
        elif com == "4":
            print(fa.get_alphabet())
        elif com == "5":
            for k in fa.get_transitions().keys():
                print("{}-> {}".format(k, fa.trans[k]))
        elif com == "6":
            print(fa.dfa())
        elif com == "t":
            sequence = input("The sequence: ")
            print(fa.check_sequence(sequence))
        else:
            print("Invalid command!")


if __name__ == '__main__':
    fa = FA("../input/FA1.txt")
    fa2 = FA("../input/IntegerFA.in")

    menu()
