from Token import *


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
        return int("".join(str(len(word) % 10) for word in self.val.split(" ")))


class Int(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"Int({self.val})"


class String(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"String({self.val})"


class Bool(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"String({self.val})"


class Print(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"Print({self.val})"


class Prev(Node):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Prev({self.name})"

    def get(self, prev, **kwargs):
        if prev.val is None:
            raise Exception("No variable was accessed before")
        return kwargs[prev.val]


class Compound(Node):

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self):
        children = ",\n    ".join(str(child).replace("    ", "        ") for child in self.children)
        return "Compound(\n    {0}\n    )".format(children)

    def __repr__(self):
        return str(self)
