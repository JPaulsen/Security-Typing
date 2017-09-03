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


def solveSecurityType(expr):
    if (expr[0].value() == "function"):
        return SecurityType(solveFunctionType(expr), SecurityLabel(expr[1].value()))
    else:
        return SecurityType(solveNativeType(expr[0].value()), SecurityLabel(expr[1].value()))


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
        returnType = solveSecurityType(expr[2])
        parameterTypes = []
        for parameter in expr[3].value():
            parameterTypes.append(solveSecurityType(parameter))
        return FunctionType(returnType, parameterTypes)
    except:
        raise ValueError(str(expr) + 'is not a valid type.')


class SecurityType:
    def __init__(self, type, securityLabel):
        self.type = type
        self.securityLabel = securityLabel

    def __str__(self):
        return "(" + str(self.type) + ", " + str(self.securityLabel) + ")"


class SecurityLabel:
    lattice = {
        "s": 0,
        "l": 1,
        "h": 2,
        "t": 3,
    }

    def __init__(self, type):
        self.type = type
        self.value = SecurityLabel.lattice[type]

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __str__(self):
        return self.type

    @staticmethod
    def join(securityLabel1, securityLabel2):
        if (securityLabel1 >= securityLabel2):
            return securityLabel1
        else:
            return securityLabel2

    @staticmethod
    def joinMultiple(securityLabels):
        return reduce(SecurityLabel.join, securityLabels, SecurityLabel("s"))

    @staticmethod
    def meet(securityLabel1, securityLabel2):
        if (securityLabel1 <= securityLabel2):
            return securityLabel1
        else:
            return securityLabel2

    @staticmethod
    def meetMultiple(securityLabels):
        return reduce(SecurityLabel.meet, securityLabels, SecurityLabel("t"))
