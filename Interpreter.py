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
    

class __Break__(object):
    
    def __init__(self):
        self.active = False

    def __bool__(self):
        return self.active


class __Return__(object):

    def __init__(self):
        self.active = False
        self.val = None

    def __bool__(self):
        return self.active


class Interpreter(object):

    def __init__(self, program):
        self.parser = Parser(program)
        pprint(self.parser.tokens)
        self.tree = self.parser.program()

    def visit(self, node, prev, scope, _break, _return, loop, function):
        if _break or _return:
            return
        
        if isinstance(node, Compound):
            for child in node.children:
                self.visit(child, prev, scope, _break, _return, loop, function)
        elif isinstance(node, While):
            __break = __Break__()
            while self.visit(node.condition, prev, scope, _break, _return, loop, function):
                self.visit(node.child, prev, scope, __break, _return, True, function)
                if __break:
                    break

        elif isinstance(node, For):
            if node.start is not None:
                scope[node.var.name] = self.visit(node.start, prev, scope, _break, _return, loop, function)
                start = self.visit(node.start, prev, scope, _break, _return, loop, function)
            else:
                scope[node.var.name] = 0
                start = 0

            end = self.visit(node.end, prev, scope, _break, _return, loop, function)
            __break = __Break__()

            for i in range(int(start), int(end)):
                prev.val = node.var.name
                self.visit(node.child, prev, scope, __break, _return, True, function)
                if __break:
                    break
                scope[node.var.name] += INT(1)
        elif isinstance(node, If):
            if self.visit(node.condition, prev, scope, _break, _return, loop, function):
                self.visit(node.child, prev, scope, _break, _return, loop, function)
            elif node.alternative is not None:
                self.visit(node.alternative, prev, scope, _break, _return, loop, function)

        elif isinstance(node, Print):
            print(self.visit(node.val, prev, scope, _break, _return, loop, function))
        elif isinstance(node, Break):
            if not loop:
                raise Exception(f"Cannot break from this location node")
            _break.active = True
        elif isinstance(node, Assign):
            if not (isinstance(node.left, Var) or isinstance(node.left, Prev)):
                # this cannot happen if the lexer and the parser are programmed correctly...
                raise Exception(f"Invalid assignment variable: {node.left}")

            if isinstance(node.left, Prev):
                node.left.name = prev.val

            prev.val = node.left.name

            if node.op in ["STR ASSIGN", "INT ASSIGN", "OBJ ASSIGN"]:
                scope[node.left.name] = self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "IADD":
                scope[node.left.name] += self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "ISUB":
                scope[node.left.name] -= self.visit(node.right, prev, scope, _break, _return, loop, function)
            else:
                raise Exception(f"Operation not added for Assign: {node.op}")

        elif isinstance(node, BinOp):
            if node.op == "ADD":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) + self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "SUB":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) - self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "MUL":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) * self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "DIV":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) / self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "OR":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) | self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "AND":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) & self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "LT":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) < self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "LEQ":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) <= self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "GT":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) > self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "GEQ":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) >= self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "NEQ":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) != self.visit(node.right, prev, scope, _break, _return, loop, function)
            elif node.op == "EQ":
                return self.visit(node.left, prev, scope, _break, _return, loop, function) == self.visit(node.right, prev, scope, _break, _return, loop, function)
            else:
                raise Exception(f"Operation not added for BinOp: {node.op}")

        elif isinstance(node, UnOp):
            if node.op == "NOT":
                val = self.visit(node.right, prev, scope, _break, _return, loop, function)
                if isinstance(val, INT) or isinstance(val, REAL):
                    return INT(-1) * val
                else:
                    return not val

        elif isinstance(node, Call):
            to_call = scope[node.name]

            if not isinstance(to_call, FUNCTION):
                raise TypeError(f"{node.name} is not a FUNCTION")

            elif len(to_call.arguments) != len(node.arguments):
                raise TypeError(f"Expected {len(to_call.arguments)} arguments, got {len(node.arguments)}")

            new_scope = dict(scope)
            for i in range(len(to_call.arguments)):
                new_scope[to_call.arguments[i]] = self.visit(node.arguments[i], prev, scope, _break, _return, loop, function)

            new_prev = __Prev__()
            new_break = __Break__()
            new_return = __Return__()
            self.visit(to_call.child, new_prev, new_scope, new_break, new_return, loop, True)
            return new_return.val

        elif isinstance(node, Return):
            if not function:
                raise Exception(f"Cannot return from current location")

            _return.val = self.visit(node.child, prev, scope, _break, _return, loop, function)
            _return.active = True

        elif isinstance(node, Bool):
            return node.val
        elif isinstance(node, String):
            return node.val
        elif isinstance(node, Int):
            return node.val
        elif isinstance(node, Real):
            return node.val
        elif isinstance(node, Object):
            return node.get(prev, **scope)
        elif isinstance(node, Var):
            prev.val = node.name
            return scope[node.name]
        elif isinstance(node, Prev):
            return node.get(prev, **scope)
        elif isinstance(node, FunctionAssign):
            scope[node.name.name] = FUNCTION([arg for arg in node.arguments], node.child)
        else:
            raise Exception(f"Node type not added: {type(node)}")

    def run(self):
        prev = __Prev__()
        _break = __Break__()
        _return = __Return__()
        scope = {}
        self.visit(self.tree, prev, scope, _break, _return, False, False)

        print("---------------------------END------------------------------")
        # pprint(scope)


if __name__ == '__main__':
    with open("program.va", "r") as f:
        interpreter = Interpreter(f.read())
    print(interpreter.tree)

    print("---------------------------RUN------------------------------")
    interpreter.run()
