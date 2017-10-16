class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __str__(self):
        return "function " + str(self.returnType) + " [" + ", ".join(map(str, self.parameterTypes)) + "]"


class SecurityType:
    def __init__(self, type, securityLabel):
        self.type = type
        self.securityLabel = securityLabel

    def __str__(self):
        return "(" + str(self.type) + ", " + str(self.securityLabel) + ")"


class SecurityLabel:
    lattice = {
        "b": 0,
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
        return reduce(SecurityLabel.join, securityLabels, SecurityLabel("b"))

    @staticmethod
    def meet(securityLabel1, securityLabel2):
        if (securityLabel1 <= securityLabel2):
            return securityLabel1
        else:
            return securityLabel2

    @staticmethod
    def meetMultiple(securityLabels):
        return reduce(SecurityLabel.meet, securityLabels, SecurityLabel("t"))
