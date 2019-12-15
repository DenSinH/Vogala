

class INT(object):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"INT({self.val})"

    def __add__(self, other):
        if isinstance(other, REAL):
            return REAL(self.val + other.val)
        elif isinstance(other, INT):
            return INT(self.val + other.val)
        raise TypeError(f"cannot add variables of types INT and {type(other)}")

    def __mul__(self, other):
        if isinstance(other, REAL):
            return REAL(self.val * other.val)
        elif isinstance(other, INT):
            return INT(self.val * other.val)
        raise TypeError(f"cannot add variables of types INT and {type(other)}")

    def __sub__(self, other):
        if isinstance(other, REAL):
            return REAL(self.val - other.val)
        elif isinstance(other, INT):
            return INT(self.val - other.val)
        raise TypeError(f"cannot add variables of types INT and {type(other)}")

    def __truediv__(self, other):
        return REAL(self.val / other.val)
    
    def __bool__(self):
        return self.val != 0

    def __int__(self):
        return self.val
    
    def __and__(self, other):
        return BOOL(bool(self) & bool(other))
    
    def __or__(self, other):
        return BOOL(bool(self) | bool(other))
    
    def __eq__(self, other):
        return BOOL(self.val == other.val)
    
    def __ne__(self, other):
        return BOOL(self.val != other.val)
    
    def __le__(self, other):
        return BOOL(self.val <= other.val)
    
    def __ge__(self, other):
        return BOOL(self.val >= other.val)
    
    def __lt__(self, other):
        return BOOL(self.val < other.val)
    
    def __gt__(self, other):
        return BOOL(self.val > other.val)
    

class BOOL(object):
    
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"BOOL({self.val})"

    def __bool__(self):
        return self.val

    def __or__(self, other):
        return BOOL(self.val | bool(other))

    def __and__(self, other):
        return BOOL(self.val & bool(other))

    def __add__(self, other):
        return self & other


class REAL(object):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"REAL({self.val})"

    def __add__(self, other):
        return REAL(self.val + other.val)

    def __mul__(self, other):
        return REAL(self.val * other.val)

    def __sub__(self, other):
        return REAL(self.val - other.val)

    def __truediv__(self, other):
        return REAL(self.val / other.val)

    def __int__(self):
        return int(self.val)

    def __bool__(self):
        return self.val != 0

    def __and__(self, other):
        return BOOL(bool(self) & bool(other))

    def __or__(self, other):
        return BOOL(bool(self) | bool(other))

    def __eq__(self, other):
        return BOOL(self.val == other.val)

    def __ne__(self, other):
        return BOOL(self.val != other.val)

    def __le__(self, other):
        return BOOL(self.val <= other.val)

    def __ge__(self, other):
        return BOOL(self.val >= other.val)

    def __lt__(self, other):
        return BOOL(self.val < other.val)

    def __gt__(self, other):
        return BOOL(self.val > other.val)


class STRING(object):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"STRING({self.val})"

    def __bool__(self):
        return self.val != ""

    def __and__(self, other):
        return BOOL(bool(self) & bool(other))

    def __or__(self, other):
        return BOOL(bool(self) | bool(other))

    def __eq__(self, other):
        return BOOL(self.val == other.val)

    def __ne__(self, other):
        return BOOL(self.val != other.val)

    def __le__(self, other):
        return BOOL(self.val <= other.val)

    def __ge__(self, other):
        return BOOL(self.val >= other.val)

    def __lt__(self, other):
        return BOOL(self.val < other.val)

    def __gt__(self, other):
        return BOOL(self.val > other.val)


class FUNCTION(object):

    def __init__(self, arguments, child):
        self.arguments = arguments
        self.child = child

    def __repr__(self):
        return f"{', '.join(self.arguments)} => {self.child}"

    def __bool__(self):
        return True
