from Lab5.src.Grammar import Grammar
from Lab5.src.LR0 import LR0


def menu():
    while True:
        print("\n1: Show all terminals")
        print("2: Show all non terminals")
        print("3: Show all productions")
        print("4: Show productions for non terminal")
        print("x: exit")
        com = input("->")
        if com == "x":
            break
        elif com == "1":
            print(grammar.get_terminals())
        elif com == "2":
            print(grammar.get_non_terminals())
        elif com == "3":
            print(grammar.get_productions())
        elif com == "4":
            n_t = input("non terminal: ")
            print(grammar.get_productions_for(n_t))
        else:
            print("Invalid command!")


if __name__ == '__main__':
    grammar = Grammar("../input/Grammar2.txt")
    lr0 = LR0(grammar)
    print(lr0.create_parsing_table())
    print(lr0.parse("a b b c"))

    menu()
