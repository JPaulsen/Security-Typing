class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __eq__(self, other):
        if other == None or not isinstance(other, FunctionType):
            return False
        parametersLength = len(self.parameterTypes)
        ans = self.returnType.type == other.returnType.type and parametersLength == len(other.parameterTypes)
        if not ans:
            return False
        for i in range(parametersLength):
            if self.parameterTypes[i].type != other.parameterTypes[i].type:
                return False
        return True

    def __le__(self, other):
        return self == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "function " + str(self.returnType) + " [" + ", ".join(map(str, self.parameterTypes)) + "]"


class SecurityType:
    def __init__(self, type, securityLabel):
        self.type = type
        self.securityLabel = securityLabel

    def __eq__(self, other):
        if other == None or not isinstance(other, SecurityType):
            return False
        return self.type == other.type and self.securityLabel == other.securityLabel

    def __lt__(self, other):
        if other == None or not isinstance(other, SecurityType):
            return False
        return self.type == other.type and self.securityLabel < other.securityLabel

    def __le__(self, other):
        if other == None or not isinstance(other, SecurityType):
            return False
        return self.type == other.type and self.securityLabel <= other.securityLabel

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

    def __eq__(self, other):
        if other == None or not isinstance(other, SecurityLabel):
            return False
        return self.value == other.value

    def __lt__(self, other):
        if other == None or not isinstance(other, SecurityLabel):
            return False
        return self.value < other.value

    def __le__(self, other):
        if other == None or not isinstance(other, SecurityLabel):
            return False
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

class RefType(SecurityType):
    def __init__(self, referencedSecurityType):
        SecurityType.__init__(self, referencedSecurityType.type, referencedSecurityType.securityLabel)
        self.referencedSecurityType = referencedSecurityType

    def __eq__(self, other):
        if other == None or not isinstance(other, RefType):
            return False
        return self.referencedSecurityType == other.referencedSecurityType

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "<ref " + str(self.referencedSecurityType) + ">"
