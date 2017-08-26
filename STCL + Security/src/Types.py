class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __eq__(self, other):
        if other == None:
            return False
        parametersLength = len(self.parameterTypes)
        ans = self.returnType.type == other.returnType.type and parametersLength == len(other.parameterTypes)
        if not ans:
            return False
        for i in range(parametersLength):
            if self.parameterTypes[i].type != other.parameterTypes[i].type:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "function " + str(self.returnType) + " [" + ", ".join(map(str, self.parameterTypes)) + "]"


def solvePairType(expr):
    if (expr[0].value() == "function"):
        return PairType(solveFunctionType(expr), SecurityType(expr[1].value()))
    else:
        return PairType(solveNativeType(expr[0].value()), SecurityType(expr[1].value()))


def solveNativeType(expr):
    if expr == "str":
        return str
    elif expr == "bool":
        return bool
    elif expr == "int":
        return int
    elif expr == "float":
        return float
    else:
        raise ValueError(expr + 'is not a valid type.')


def solveFunctionType(expr):
    try:
        returnType = solvePairType(expr[2])
        parameterTypes = []
        for parameter in expr[3].value():
            parameterTypes.append(solvePairType(parameter))
        return FunctionType(returnType, parameterTypes)
    except:
        raise ValueError(str(expr) + 'is not a valid type.')


class PairType:
    def __init__(self, type, securityType):
        self.type = type
        self.securityType = securityType

    def __str__(self):
        return "(" + str(self.type) + ", " + str(self.securityType) + ")"


class SecurityType:
    lattice = {
        "s": 0,
        "l": 1,
        "h": 2,
        "t": 3,
    }

    def __init__(self, type):
        self.type = type
        self.value = SecurityType.lattice[type]

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __str__(self):
        return self.type

    @staticmethod
    def join(securityType1, securityType2):
        if (securityType1 >= securityType2):
            return securityType1
        else:
            return securityType2

    @staticmethod
    def joinMultiple(securityTypes):
        return reduce(SecurityType.join, securityTypes, SecurityType("s"))

    @staticmethod
    def meet(securityType1, securityType2):
        if (securityType1 <= securityType2):
            return securityType1
        else:
            return securityType2

    @staticmethod
    def meetMultiple(securityTypes):
        return reduce(SecurityType.meet, securityTypes, SecurityType("t"))
