from ParserUtils import *
from Types import *


def parseType(expr):
    if (expr[0].value() == "function"):
        checkLengthExpected("Function type", expr, 3)
        return parseFunctionTypeFromTypeExpression(expr)
    else:
        checkLengthExpected("Native type", expr, 1)
        return parseNativeType(expr[0].value())


def parseNativeType(expr):
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


def parseFunctionTypeFromTypeExpression(expr):
    return _parseFunctionType(expr[1], expr[2].value())


def parseFunctionTypeFromNodeExpression(expr):
    return _parseFunctionType(expr[1], map(_getFirst, expr[2].value()))


def _getFirst(touple):
    return touple[0]


def _parseFunctionType(returnTypeExpression, parameterTypesExpression):
    return FunctionType(parseType(returnTypeExpression), map(parseType, parameterTypesExpression))
