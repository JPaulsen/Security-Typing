class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __str__(self):
        return "function " + str(self.returnType) + " [" + ", ".join(map(str, self.parameterTypes)) + "]"


class RefType:
    def __init__(self, referencedType):
        self.referencedType = referencedType

    def __str__(self):
        return "<ref " + str(self.referencedType) + ">"
