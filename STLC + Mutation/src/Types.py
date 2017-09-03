class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __eq__(self, other):
        if other == None or not isinstance(other, FunctionType):
            return False
        parametersLength = len(self.parameterTypes)
        ans = self.returnType == other.returnType and parametersLength == len(other.parameterTypes)
        if not ans:
            return False
        for i in range(parametersLength):
            if self.parameterTypes[i] != other.parameterTypes[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "function " + str(self.returnType) + " [" + ", ".join(map(str, self.parameterTypes)) + "]"


class RefType:
    def __init__(self, referencedType):
        self.referencedType = referencedType

    def __eq__(self, other):
        if other == None or not isinstance(other, RefType):
            return False
        return self.referencedType == other.referencedType

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "<ref " + str(self.referencedType) + ">"
