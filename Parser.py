from Lexer import Lexer
from Token import *
from AST import *

from pprint import pprint


class Parser(object):

    def __init__(self, program):
        self.lexer = Lexer(program)
        self.tokens = self.lexer.tokenize()

        self.cursor = 0
        if self.tokens:
            self.current = self.tokens[self.cursor]
        else:
            self.current = None

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

    def func(self):
        name = self.current.val
        self.expect("FUNC")

        self.expect("CALL")
        arguments = []
        while self.current.typ not in ENDING + LOOPING:
            arguments.append(self.weak())
            if self.current.typ not in ENDING + LOOPING:
                self.expect(",")
        return Call(name, arguments)

    def prev(self):
        node = Prev(self.current.val)
        self.expect("PREV")
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
        elif self.current.typ == "FUNC":
            return self.func()
        elif self.current.typ == "INT":
            node = Int(self.current.val)
            self.expect(*FACTORS)
        elif self.current.typ == "REAL":
            node = Real(self.current.val)
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

        while self.current.typ not in ENDING + LOOPING + [","]:
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
        elif op in ENDING + WEAKOP + LOOPING + [","]:
            return left
        else:
            raise Exception(f"Invalid Syntax near {self.current.val}")

    def statement(self):
        if self.current.typ == "ID":
            left = self.variable()
            op = self.current.typ
            if self.current.typ in ASSIGNMENT:
                if self.current.typ == "FUNC ASSIGN":
                    self.expect(*ASSIGNMENT)
                    arguments = []
                    while self.current.typ != "END":
                        arguments.append(self.current.val)
                        self.expect("ID")
                    self.expect("END")

                    return FunctionAssign(left, arguments, self.compound_statement())

                self.expect(*ASSIGNMENT)
                return Assign(left, op, self.weak())

            elif self.current.typ == "GOES":
                self.expect("GOES")
                if self.current.typ == "FROM":
                    self.expect("FROM")
                    start = self.weak()
                else:
                    start = None

                self.expect("TO")
                end = self.weak()
                self.expect("END")
                return For(left, start, end, self.compound_statement())
            else:
                raise Exception(f"Expected one of {', '.join(ASSIGNMENT)} or GOES, got {self.current.typ}, {self.current.val}")

        elif self.current.typ == "FUNC":
            return self.func()

        elif self.current.typ == "IF":
            self.expect("IF")
            condition = self.weak()
            self.expect("END")
            child = self.compound_statement()

            alternative = None
            if self.current.typ == "ELSE":
                self.expect("ELSE")
                self.expect("END")
                alternative = self.compound_statement()

            return If(condition, child, alternative)

        elif self.current.typ == "PREV":
            left = self.prev()
            op = self.current.typ
            self.expect(*ASSIGNMENT)
            return Assign(left, op, self.weak())

        elif self.current.typ == "PRINT":
            self.expect("PRINT")
            return Print(self.weak())

        elif self.current.typ == "BREAK":
            self.expect("BREAK")
            return Break()

        elif self.current.typ == "RETURN":
            self.expect("RETURN")
            val = None
            if self.current.typ not in ENDING:
                val = self.weak()
            return Return(val)

        elif self.current.typ == "WHILE":
            self.expect("WHILE")
            condition = self.weak()
            if self.current.typ == "DO":
                self.expect("DO")
            self.expect("END")
            return While(condition, self.compound_statement())

        elif self.current.typ in FACTORS:
            return self.weak()
        else:
            raise Exception(f"Syntax error near {self.current.val}")

    def compound_statement(self):
        children = []
        while self.current is not None and self.current.typ != "LOCAL END":
            children.append(self.statement())

            # we have already expected the local end for some statements
            if not any(isinstance(children[-1], node) for node in (For, While, FunctionAssign, If)):
                if self.current is not None and self.current.typ != "LOCAL END":
                    self.expect("END")

        if self.current is not None:
            self.expect("LOCAL END")

        return Compound(*children)

    def program(self):
        children = []
        while self.current is not None:
            children.append(self.compound_statement())

        return Compound(*children)


if __name__ == '__main__':
    parser = Parser()
    print(parser.program())
