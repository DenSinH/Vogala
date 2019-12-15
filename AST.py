from Token import *
from Vartypes import *


class Node(object):
    pass


class BinOp(Node):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left} {self.op} {self.right})"


class UnOp(Node):

    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __str__(self):
        return f"UnOp({self.op} {self.right})"


class Assign(Node):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"Assign({self.left} {self.op} {self.right})"


class Var(Node):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Var({self.name})"


class Call(Node):

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return f"Call({self.name}(\n    {', '.join(str(arg) for arg in self.arguments)}\n    ) )"


class Object(Node):

    def __init__(self, val):
        """ May be interpreted as either INT or ID or REAL or VAR(or STR if added to a STR) (or function call)"""
        self.val = val

    def __str__(self):
        return f"Object({self.val})"

    def get(self, prev, **kwargs):
        if self.val in kwargs:
            prev.val = self.val
            return kwargs[self.val]
        return INT(int("".join(str(len(word) % 10) for word in self.val.split(" "))))


class Int(Node):

    def __init__(self, val):
        self.val = INT(val)

    def __str__(self):
        return f"Int({self.val})"


class Real(Node):

    def __init__(self, val):
        self.val = REAL(val)

    def __str__(self):
        return f"Real({self.val})"


class String(Node):

    def __init__(self, val):
        self.val = STRING(val)

    def __str__(self):
        return f"String({self.val})"


class Bool(Node):

    def __init__(self, val):
        self.val = BOOL(val)

    def __str__(self):
        return f"String({self.val})"


class FunctionAssign(Node):

    def __init__(self, name, arguments, child):
        self.name = name
        self.arguments = arguments
        self.child = child

    def __str__(self):
        return f"FunctionAssign({self.name}: {', '.join(str(arg) for arg in self.arguments)} => \n    {self.child}\n    )"


class Print(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"Print({self.val})"


class Break(Node):

    def __str__(self):
        return f"Break"


class Return(Node):

    def __init__(self, child):
        self.child = child

    def __str__(self):
        return f"Return({self.child})"


class Prev(Node):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Prev({self.name})"

    def get(self, prev, **kwargs):
        if prev.val is None:
            raise Exception("No variable was accessed before")
        return kwargs[prev.val]


class While(Node):

    def __init__(self, condition, child):
        self.condition = condition
        self.child = child

    def __str__(self):
        return f"While({self.condition}: \n    {self.child}\n    )"


class For(Node):

    def __init__(self, var, start, end, child):
        self.var = var
        self.start = start or Int(0)
        self.end = end
        self.child = child

    def __str__(self):
        return f"For({self.var.name}\n    FROM {self.start}\n    TO {self.end}\n    : {self.child})"


class If(Node):

    def __init__(self, condition, child, alternative):
        self.condition = condition
        self.child = child
        self.alternative = alternative

    def __str__(self):
        return f"If({self.condition}\n    ? {self.child}\n    : {self.alternative})"


class Compound(Node):

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self):
        children = ",\n    ".join(str(child).replace("    ", "        ") for child in self.children)
        return "Compound(\n    {0}\n    )".format(children)

    def __repr__(self):
        return str(self)
