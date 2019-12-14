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

    def check_name(self, name):
        if name in self.kws:
            raise Exception(f"Variable name not allowed: {name}, reserved keyword.")

    def tokenize(self):
        tokens = []

        while self.current is not None:

            if self.kws.get(self.current) in OPENERS:
                if self.kws[self.current] == "PRINT":
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()

                    tokens += self.expr()

                elif self.kws[self.current] == "WHILE":
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()

                    tokens += self.expr()

                    if self.kws.get(self.current) == "DO":
                        tokens.append(Token(self.kws[self.current], self.current))
                        self.advance()

                elif self.kws[self.current] == "IF":
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()

                    tokens += self.expr()

                elif self.kws[self.current] == "ELSE":
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()

                else:
                    raise Exception(f"No opening statement added for {self.current}")

                if self.kws[self.current] in ENDING:
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()
                else:
                    raise Exception(f"Expected statement end after {self.current}")

            elif self.kws.get(self.current) is not None:
                raise SyntaxError(f"Invalid syntax near '{self.current}'")

            else:
                ahead = self.look_ahead()
                if self.kws.get(ahead) in ASSIGNMENT:
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

                    else:
                        raise Exception(f"Expected assignment at {self.current}")

                elif self.kws.get(ahead) in LOOPING:
                    if self.kws[ahead] == "GOES":
                        name = self.id()
                        self.check_name(name)
                        tokens.append(Token("ID", name))

                        if self.kws.get(self.current) != "GOES":
                            raise Exception(f"Expected GOES, got {self.current}")

                        tokens.append(Token(self.kws[self.current], self.current))
                        self.advance()

                        if self.kws.get(self.current) == "FROM":
                            tokens.append(Token(self.kws[self.current], self.current))
                            self.advance()

                            tokens += self.expr()

                        if self.kws.get(self.current) == "TO":
                            tokens.append(Token(self.kws[self.current], self.current))
                            self.advance()

                            tokens += self.expr()
                        else:
                            raise Exception(f"Expected TO, got {self.current}")

                else:
                    tokens += self.expr()
                    continue

                if self.kws[self.current] in ENDING:
                    tokens.append(Token(self.kws[self.current], self.current))
                    self.advance()
                    while self.kws.get(self.current) in ENDING:
                        self.advance()
                else:
                    raise Exception(f"Expected statement end after {self.current}")

        return tokens

    def id(self):
        name = ""
        while self.kws.get(self.current) not in ASSIGNMENT + ENDING + LOOPING:
            name += f" {self.current}"
            self.advance()

            if self.current is None:
                raise EOFError("End of file while scanning variable name")

        try:
            int(name.strip()[0])
            raise Exception(f"Variable names cannot start with integers: {name.strip()}")
        except ValueError:
            return name.strip()

    def string(self, start=None):
        s = []
        while (start is None and self.kws.get(self.current) not in ENDING) or self.current != start:
            s.append(self.current)
            self.advance()

        if start is None:
            return [Token("STR", " ".join(s))]

        self.advance()  # pass over ending quote
        return Token("STR", " ".join(s))

    def expr(self):
        expr = []

        while True:
            factor = []
            if self.current in "'\"":
                start = str(self.current)
                self.advance()
                expr.append(self.string(start))

            while self.kws.get(self.current) not in STRONGOP + WEAKOP + UNOP + ENDING + LOOPING:
                factor.append(self.current)
                self.advance()

            if any(factor):
                expr.append(Token("OBJ", " ".join(factor)))

            if self.kws[self.current] in ENDING:
                break
            elif self.kws[self.current] in LOOPING:
                break

            expr.append(Token(self.kws[self.current], self.current))
            self.advance()

        return expr


if __name__ == '__main__':
    lexer = Lexer()
    print(lexer.program)
    pprint(lexer.tokenize())
