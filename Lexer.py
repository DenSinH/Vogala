from Token import *

import re
import json
from pprint import pprint


def starts_with(lst, sublst):
    if len(sublst) > len(lst):
        return False
    else:
        return lst[:len(sublst)] == sublst


class Lexer(object):

    def __init__(self):
        with open("keywords.json", "r") as f:
            self.kws = json.load(f)

        with open("program.va", "r") as f:
            program = re.sub(r"\s+", " ", f.read().upper())

        self.program = [word.strip() for word in re.split(r"(\W)", program) if word.strip()]
        self.cursor = 0
        self.current = self.get_after() or self.program[self.cursor]

    def advance(self):
        if self.current is None:
            raise EOFError("Use statement end operators! (.?:;! ...)")

        self.cursor += len(split(self.current))
        if self.cursor < len(self.program):
            self.current = self.get_after() or self.program[self.cursor]
        else:
            self.current = None

    def get_after(self, start=None):
        if start is None:
            start = int(self.cursor)

        for kw in sorted(self.kws, key=lambda _kw: len(split(_kw)), reverse=True):
            if starts_with(self.program[start:], split(kw)):
                return kw
        return None

    def look_ahead(self):
        cur = int(self.cursor)
        while self.get_after(cur) is None:
            cur += 1
        return self.get_after(cur)

    def tokenize(self):
        tokens = []

        while self.current is not None:

            if self.kws.get(self.current) in OPENERS:
                if self.kws.get(self.current) == "PRINT":
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()

                    tokens += self.expr()

            elif self.kws.get(self.current) is not None:
                raise SyntaxError(f"Invalid syntax near '{self.current}'")

            else:
                ahead = self.look_ahead()
                if self.kws.get(ahead) not in ASSIGNMENT:
                    tokens += self.expr()
                    continue

                name = self.id()
                if name in VARS["PREV"]:
                    tokens.append(Token("PREV", None))
                else:
                    tokens.append(Token("ID", name))
                tokens.append(Token(self.kws[self.current], self.current))

                if self.kws[self.current] == "OBJ ASSIGN":
                    self.advance()
                    tokens += self.expr()

                elif self.kws[self.current] == "STR ASSIGN":
                    self.advance()
                    tokens += self.string()

                elif self.kws[self.current] == "IADD":
                    self.advance()
                    tokens += self.expr()

        return tokens

    def id(self):
        name = ""
        while self.kws.get(self.current) not in ASSIGNMENT + ENDING:
            name += f" {self.current}"
            self.advance()

            if self.current is None:
                raise EOFError("End of file while scanning variable name")

        return name.strip()

    def string(self, start=None):
        s = []
        while (start is None and self.kws.get(self.current) not in ENDING) or self.current != start:
            s.append(self.current)
            self.advance()

        if start is None:
            end = Token(self.kws[self.current], self.current)
            self.advance()
            return [Token("STR", " ".join(s)), end]

        self.advance()
        return Token("STR", " ".join(s))

    def expr(self):
        expr = []

        while True:
            factor = []
            if self.current in "'\"":
                start = str(self.current)
                self.advance()
                expr.append(self.string(start))

            while self.kws.get(self.current) not in STRONGOP + WEAKOP + UNOP + ENDING:
                factor.append(self.current)
                self.advance()

            if any(factor):
                expr.append(Token("OBJ", " ".join(factor)))

            expr.append(Token(self.kws[self.current], self.current))
            if self.kws[self.current] in ["END", "LOCAL END"]:
                self.advance()
                break

            self.advance()

        return expr


if __name__ == '__main__':
    lexer = Lexer()
    print(lexer.program)
    pprint(lexer.tokenize())
