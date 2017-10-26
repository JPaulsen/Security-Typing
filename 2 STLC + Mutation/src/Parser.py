from AST import *
from sexpdata import *
from TypeParser import *


def parse(expr):
    if len(expr) == 0:
        raise ValueError('expressions can not be empty.')
    command = expr[0]
    if not isinstance(command, Symbol):
        raise ValueError('first keyword of a expression must be a symbol.')
    command = command.value()
    if command == 'bool':
        checkLengthExpected("Boolean literal", expr, 2)
        value = expr[1]
        return BoolLiteral(value)
    elif command == 'int':
        checkLengthExpected("Integer literal", expr, 2)
        value = expr[1]
        return IntLiteral(value)
    elif command == 'float':
        checkLengthExpected("Float literal", expr, 2)
        value = expr[1]
        return FloatLiteral(value)
    elif command == 'str':
        checkLengthExpected("String literal", expr, 2)
        value = expr[1]
        return StringLiteral(value)
    elif command == "not":
        checkLengthExpected("not", expr, 2)
        expression = parse(expr[1])
        return UnaryExpression("not", expression)
    elif command == "and" or command == "or" or command == "+" or command == "-" or command == "*" or command == "/":
        checkLengthExpected(command, expr, 3)
        firstExpression = parse(expr[1])
        secondExpression = parse(expr[2])
        return BinaryExpression(command, firstExpression, secondExpression)
    elif command == "if":
        checkLengthExpected("if", expr, 4)
        conditionExpression = parse(expr[1])
        thenExpression = parse(expr[2])
        elseExpression = parse(expr[3])
        return IfExpression(conditionExpression, thenExpression, elseExpression)
    elif command == "let":
        checkLengthExpected("let", expr, 4)
        symbol = expr[1]
        if not isinstance(symbol, Symbol):
            raise ValueError('let first argument must be a symbol.')
        valueExpression = parse(expr[2])
        thenExpression = parse(expr[3])
        return LetExpression(symbol, valueExpression, thenExpression)
    elif command == "function":
        checkLengthExpected("function", expr, 4)
        functionType = parseFunctionType(expr)
        parameterSymbols = map(_getSecond, expr[2].value())
        parametersLength = len(parameterSymbols)
        if parametersLength != len(functionType.parameterTypes):
            raise ValueError('Function length of types and parameters do not match.')
        for i in range(parametersLength):
            symbol = parameterSymbols[i]
            if not isinstance(symbol, Symbol):
                raise ValueError('Each function parameter must be a symbol.')
        bodyExpression = parse(expr[3])
        return FunctionExpression(functionType, parameterSymbols, bodyExpression)
    elif command == "apply":
        checkLengthExpected("apply", expr, 3)
        functionExpression = parse(expr[1])
        argumentExpressions = []
        for argumentExpression in expr[2].value():
            argumentExpressions.append(parse(argumentExpression))
        return ApplyExpression(functionExpression, argumentExpressions)
    elif command == "ref":
        checkLengthExpected("ref", expr, 2)
        return RefExpression(parseType(expr[1]))
    elif command == "deref":
        checkLengthExpected("deref", expr, 2)
        return DerefExpression(parse(expr[1]))
    elif command == "assign":
        checkLengthExpected("assign", expr, 4)
        return AssignmentExpression(parse(expr[1]), parse(expr[2]), parse(expr[3]))
    else:
        checkLengthExpected("variable use", expr, 1)
        return GetExpression(expr[0])


def _getSecond(tuple):
    return tuple[1]
