import re

from Lab3.src.PIF import PIFEntry, PIF
from Lab3.src.SortedTable import SortedTable
from Lab3.src.Tokanizer import Tokenizer

if __name__ == '__main__':

    with open("Lab3/input/p{}.in".format(2), "r") as f:
        program = f.read()

    tk = Tokenizer()

    tokens = tk.tokenize(program)

    # print(tokens)

    st = SortedTable()
    pif = PIF()

    with open("Lab3/input/keywords.in", "r") as f:
        keywords = f.read().split()

    integers = re.compile(r"0|[1-9][0-9]*|[+-][1-9][0-9]*")
    strings = re.compile(r'^".*"$')
    variables = re.compile(r'[A-Z]|[a-z]\w*')

    for token in tokens:
        if token in keywords:
            pif.append(PIFEntry(token, -1))
        elif integers.fullmatch(token) or strings.fullmatch(token):  # if token is constant
            st.append(token)
            pif.append(PIFEntry("const", st.search(token)))
        elif variables.fullmatch(token):  # if token is variable
            st.append(token)
            pif.append(PIFEntry("id", st.search(token)))
        else:
            print("ERROR!")

    with open('Lab3/output/st.out', 'w') as f:
        print(st, file=f)

    with open('Lab3/output/pif.out', 'w') as f:
        print(pif, file=f)
