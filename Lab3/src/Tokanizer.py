import re


class Tokenizer:
    def __to_map(self, s):
        return re.findall(r'\w+|".*"|\s|\[|\]|\(|\)|\{|\}|\S+', s)

    def tokenize(self, string):
        string = self.__to_map(string)
        res = []
        spaces = re.compile(r"\s")
        for s in string:
            if not spaces.fullmatch(s):
                res.append(s)
        return res
