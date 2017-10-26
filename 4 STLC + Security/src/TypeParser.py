from ParserUtils import *
from Types import *


def parseFunctionSecurityType(expr):
    return SecurityType(_parseFunctionType(expr[2], map(_getFirst, expr[3].value())), SecurityLabel(expr[1].value()))


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


def parseSecurityType(expr):
    if (expr[0].value() == "function"):
        checkLengthExpected("Function type", expr, 4)
        return SecurityType(_parseFunctionTypeFromTypeExpression(expr), SecurityLabel(expr[1].value()))
    else:
        checkLengthExpected("Native type", expr, 2)
        return SecurityType(parseNativeType(expr[0].value()), SecurityLabel(expr[1].value()))


def _getFirst(touple):
    return touple[0]


def _parseFunctionType(returnTypeExpression, parameterTypesExpression):
    return FunctionType(parseSecurityType(returnTypeExpression), map(parseSecurityType, parameterTypesExpression))


def _parseFunctionTypeFromTypeExpression(expr):
    return _parseFunctionType(expr[2], expr[3].value())
