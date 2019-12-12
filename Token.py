import json
import re


with open("vars.json", "r") as f:
    VARS = json.load(f)


ASSIGNMENT = ["OBJ ASSIGN", "STR ASSIGN", "IADD", "ISUB"]
ENDING = ["END", "LOCAL END"]
BINOP = ["ADD", "SUB", "DIV", "MUL", "OR"]
UNOP = ["NOT"]
OPENERS = ["PRINT"]
FACTORS = ["OBJ", "STR", "INT", "VAR", "BOOL", "PREV"]


def split(kw):
    return [s.strip() for s in re.split(r"(\W)", kw) if s.strip()]


class Token(object):

    def __init__(self, typ, val):
        if typ == "OBJ":
            m = re.match(r"^(['\"])([^\1]*)\1$", val)
            if m is not None:
                self.typ = "STR"
                self.val = m.group(2).strip()
            elif re.match(r"^\d*$", val):
                self.typ = "INT"
                self.val = int(val)
            else:
                for TYP in VARS:
                    if val in VARS[TYP]:
                        self.typ = TYP
                        self.val = VARS[TYP][val]
                        break
                else:
                    self.typ = typ
                    self.val = val
        else:
            self.typ = typ
            self.val = val

    def __repr__(self):
        return f"{self.typ}({self.val})"
