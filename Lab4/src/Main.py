from Lab4.src.FA import FA


def menu():
    while True:
        print("\n1: Show all states")
        print("2: Show initial state")
        print("3: Show final states")
        print("4: Show alphabet")
        print("5: Show transitions")
        print("x: exit")
        com = input("->")
        if com == "x":
            break
        elif com == "1":
            for s in fa.states:
                print(s.name)
        elif com == "2":
            print(fa.states[0].name)
        elif com == "3":
            for s in fa.states:
                if s.final:
                    print(s.name)
        elif com == "4":
            print(fa.alphabet)
        elif com == "5":
            for k in fa.trans.keys():
                print("{}: {}".format(k, fa.trans[k]))
        else:
            print("Invalid command!")


if __name__ == '__main__':
    fa = FA("../input/FA1.txt")

    menu()
