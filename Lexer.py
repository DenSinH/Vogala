import re
import json
from pprint import pprint


class Token(object):

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val


class Lexer(object):

    def __init__(self):
        slashed_chars = ".*+:?"

        with open("keywords.json", "r") as f:
            self.kws = json.load(f)

        fmat = r"(?:\A|\s)({0})(?:\s|\Z)".format("|".join("\\" + kw if kw in slashed_chars else kw for kw in self.kws if self.kws[kw] != "END"))
        self.split_statement = re.compile(fmat)

        fmat = r"{0}".format("|".join("\\" + kw if kw in slashed_chars else kw for kw in self.kws if self.kws[kw] == "END"))
        self.split_end = re.compile(fmat)

        with open("program.va", "r") as f:
            self.program = re.sub(r"\s+", " ", f.read().upper())
        pprint(self.program)

    def get_statements(self):
        prog = []
        for statement in self.split_end.split(self.program):
            prog.append([tok.strip() for tok in self.split_statement.split(f" {statement} ") if tok.strip()])
        return prog


if __name__ == '__main__':
    lexer = Lexer()
    pprint(lexer.get_statements())
