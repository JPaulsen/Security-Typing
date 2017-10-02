from ParserUtils import *
from Types import *


def parseFunctionType(expr):
    return _parseFunctionType(expr[1], map(_getFirst, expr[2].value()))


def parseNativeType(expr):
    if expr == "str":
        return str
    elif expr == "bool":
        return bool
    elif expr == "int":
        return int
    elif expr == "float":
        return float
    elif expr == "dynamic":
        return DynamicType()
    else:
        raise ValueError(expr + 'is not a valid type.')


def parseType(expr):
    if (expr[0].value() == "function"):
        checkLengthExpected("Function type", expr, 3)
        return _parseFunctionTypeFromTypeExpression(expr)
    else:
        checkLengthExpected("Native type", expr, 1)
        return parseNativeType(expr[0].value())


def _parseFunctionType(returnTypeExpression, parameterTypesExpression):
    return FunctionType(parseType(returnTypeExpression), map(parseType, parameterTypesExpression))


def _parseFunctionTypeFromTypeExpression(expr):
    return _parseFunctionType(expr[1], expr[2].value())


def _getFirst(touple):
    return touple[0]
