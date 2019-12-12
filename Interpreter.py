from Parser import Parser
from AST import *

from pprint import pprint


class __Prev__(object):

    def __init__(self):
        self.val = None

    def __repr__(self):
        return self.val

    def __str__(self):
        return self.val.__str__()


class Interpreter(object):

    def __init__(self):
        self.parser = Parser()
        pprint(self.parser.tokens)
        self.tree = self.parser.program()

    def visit(self, node, prev, scope):
        if isinstance(node, Compound):
            new_scope = dict(scope)
            new_prev = __Prev__()
            for child in node.children:
                self.visit(child, new_prev, new_scope)
            print("Compound end:", new_scope)
        elif isinstance(node, Print):
            print(self.visit(node.val, prev, scope))
        elif isinstance(node, Assign):
            if not isinstance(node.left, Var) or isinstance(node.left, Prev):
                # this cannot happen if the lexer and the parser are programmed correctly...
                raise Exception(f"Invalid assignment variable: {node.left}")

            if isinstance(node.left, Prev):
                node.left.name = prev.val

            if node.op in ["STR ASSIGN", "INT ASSIGN", "OBJ ASSIGN"]:
                scope[node.left.name] = self.visit(node.right, prev, scope)
            elif node.op == "IADD":
                scope[node.left.name] += self.visit(node.right, prev, scope)
            elif node.op == "ISUB":
                scope[node.left.name] -= self.visit(node.right, prev, scope)
            else:
                raise Exception(f"Operation not added for Assign: {node.op}")
            prev.val = node.left.name

        elif isinstance(node, BinOp):
            if node.op == "ADD":
                val = self.visit(node.left, prev, scope)
                if isinstance(val, int) and not isinstance(val, bool):
                    return val + self.visit(node.right, prev, scope)
                else:
                    return val and self.visit(node.right, prev, scope)
            elif node.op == "SUB":
                return self.visit(node.left, prev, scope) - self.visit(node.right, prev, scope)
            elif node.op == "MUL":
                return self.visit(node.left, prev, scope) * self.visit(node.right, prev, scope)
            elif node.op == "DIV":
                return self.visit(node.left, prev, scope) / self.visit(node.right, prev, scope)
            elif node.op == "OR":
                return self.visit(node.left, prev, scope) | self.visit(node.right, prev, scope)
            elif node.op == "LT":
                return self.visit(node.left, prev, scope) < self.visit(node.right, prev, scope)
            elif node.op == "GT":
                return self.visit(node.left, prev, scope) > self.visit(node.right, prev, scope)
            elif node.op == "EQ":
                return self.visit(node.left, prev, scope) == self.visit(node.right, prev, scope)
            else:
                raise Exception(f"Operation not added for BinOp: {node.op}")
        elif isinstance(node, UnOp):
            if node.op == "NOT":
                val = self.visit(node.right, prev, scope)
                if isinstance(val, int) and not isinstance(val, bool):
                    return - val
                else:
                    return not val

        elif isinstance(node, Bool):
            return node.val
        elif isinstance(node, String):
            return node.val
        elif isinstance(node, Int):
            return node.val
        elif isinstance(node, Object):
            return node.get(prev, **scope)
        elif isinstance(node, Var):
            prev.val = node.name
            return scope[node.name]
        elif isinstance(node, Prev):
            return node.get(prev, **scope)
        else:
            raise Exception(f"Node type not added: {type(node)}")

    def run(self):
        prev = None
        self.visit(self.tree, prev, {})


if __name__ == '__main__':
    interpreter = Interpreter()
    pprint(interpreter.parser.tokens)
    print(interpreter.tree)

    print("---------------------------RUN------------------------------")
    interpreter.run()
