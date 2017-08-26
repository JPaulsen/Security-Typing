from sexpdata import *


class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __eq__(self, other):
        if other == None:
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


def solveType(expr):
    if isinstance(expr, Symbol):
        expr = expr.value()
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
    try:
        if expr[0].value() == "function":
            returnType = solveType(expr[1])
            parameterTypes = []
            for parameter in expr[2].value():
                parameterTypes.append(solveType(parameter))
            return FunctionType(returnType, parameterTypes)
        else:
            raise ValueError(str(expr) + 'is not a valid type.')
    except:
        raise ValueError(str(expr) + 'is not a valid type.')
