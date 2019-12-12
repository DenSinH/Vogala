from Lexer import Lexer
from Token import *
from AST import *

from pprint import pprint


class Parser(object):

    def __init__(self):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokenize()

        self.cursor = 0
        self.current = self.tokens[self.cursor]

    def advance(self):
        self.cursor += 1
        if self.cursor >= len(self.tokens):
            self.current = None
        else:
            self.current = self.tokens[self.cursor]

    def expect(self, *typs):
        if self.current.typ not in typs:
            raise Exception(f"Invalid syntax near {self.current.val}")
        self.advance()

    def variable(self):
        node = Var(self.current.val)
        self.expect("ID")
        return node

    def factor(self):
        if self.current.typ in UNOP:
            op = self.current.typ
            self.expect(*UNOP)
            node = UnOp(op, self.factor())
        elif self.current.typ == "STR":
            node = String(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "OBJ":
            node = Object(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "VAR":
            node = Var(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "INT":
            node = Int(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "PREV":
            node = Prev(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "BOOL":
            node = Bool(self.current.val)
            self.expect(*FACTORS)
        else:
            raise Exception(f"Unexpected token: {self.current}, expected one of {UNOP + FACTORS}")
        return node

    def weak(self):
        node = self.strong()

        while self.current.typ not in ENDING:
            op = self.current.typ

            self.expect(*WEAKOP)
            node = BinOp(node, op, self.weak())

        return node

    def strong(self):
        left = self.factor()
        op = self.current.typ
        if op in STRONGOP:
            self.expect(*STRONGOP)
            return BinOp(left, op, self.strong())
        elif op in ENDING + WEAKOP:
            return left
        else:
            raise Exception(f"Invalid Syntax near {self.current.val}")

    def statement(self):
        if self.current.typ == "ID":
            left = self.variable()
            op = self.current.typ
            self.expect(*ASSIGNMENT)
            return Assign(left, op, self.weak())
        elif self.current.typ == "PRINT":
            self.expect("PRINT")
            return Print(self.weak())
        elif self.current.typ in FACTORS:
            return self.weak()
        else:
            raise Exception(f"Syntax error near {self.current.val}")

    def compound_statement(self):
        children = []
        while self.current is not None and self.current.typ != "LOCAL END":
            children.append(self.statement())
            if self.current.typ is not None and self.current.typ != "LOCAL END":
                self.expect("END")
        return Compound(*children)

    def program(self):
        children = []
        while self.current is not None:
            children.append(self.compound_statement())
            if self.current is not None:
                self.expect("LOCAL END")

        return Compound(*children)


if __name__ == '__main__':
    parser = Parser()
    print(parser.program())
