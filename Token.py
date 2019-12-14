import json
import re


with open("vars.json", "r") as f:
    VARS = json.load(f)


ASSIGNMENT = ["OBJ ASSIGN", "STR ASSIGN", "IADD", "ISUB"]
ENDING = ["END", "LOCAL END"]
STRONGOP = ["DIV", "MUL", "LT", "GT", "EQ"]
WEAKOP = ["OR", "ADD", "SUB", "AND"]
UNOP = ["NOT"]
OPENERS = ["PRINT", "WHILE"]
LOOPING = ["GOES", "FROM", "TO", "DO"]
FACTORS = ["OBJ", "STR", "INT", "REAL", "VAR", "BOOL", "PREV"]


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
            elif re.match(r".*,.*", val) and not re.match(r".*,.*,.*", val):
                self.typ = "REAL"
                v = ""
                for part in split(val):
                    if part == ",":
                        v += "."
                    else:
                        if part in VARS["INT"]:
                            v += str(VARS["INT"][part])
                        else:
                            v += str(len(part) % 10)

                self.val = float(v)
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
