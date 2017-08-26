from AST import *
from Types import *


def _checkLengthExpected(name, expr, n):
    if (len(expr) != n):
        lastPart = ' elements.'
        if (n == 1):
            lastPart = ' element.'
        raise ValueError(name + ' expressions must have ' + str(n) + lastPart)


def parse(expr):
    if (len(expr) == 0):
        raise ValueError('expressions can not be empty.')
    command = expr[0]
    if (not isinstance(command, Symbol)):
        raise ValueError('first keyword of a expression must be a symbol.')
    command = command.value()
    if (command == 'bool'):
        _checkLengthExpected("Boolean literal", expr, 2)
        value = expr[1]
        return BoolLiteral(value)
    elif (command == 'int'):
        _checkLengthExpected("Integer literal", expr, 2)
        value = expr[1]
        return IntLiteral(value)
    elif (command == 'float'):
        _checkLengthExpected("Float literal", expr, 2)
        value = expr[1]
        return FloatLiteral(value)
    elif (command == 'str'):
        _checkLengthExpected("String literal", expr, 2)
        value = expr[1]
        return StringLiteral(value)
    elif (command == "not"):
        _checkLengthExpected("not", expr, 2)
        expression = parse(expr[1])
        return UnaryExpression("not", expression)
    elif (command == "and" or command == "or" or command == "+" or command == "-" or command == "*" or command == "/"):
        _checkLengthExpected(command, expr, 3)
        firstExpression = parse(expr[1])
        secondExpression = parse(expr[2])
        return BinaryExpression(command, firstExpression, secondExpression)
    elif (command == "if"):
        _checkLengthExpected("if", expr, 4)
        conditionExpression = parse(expr[1])
        thenExpression = parse(expr[2])
        elseExpression = parse(expr[3])
        return IfExpression(conditionExpression, thenExpression, elseExpression)
    elif (command == "let"):
        _checkLengthExpected("let", expr, 4)
        symbol = expr[1]
        if (not isinstance(symbol, Symbol)):
            raise ValueError('let first argument must be a symbol.')
        valueExpression = parse(expr[2])
        thenExpression = parse(expr[3])
        return LetExpression(symbol, valueExpression, thenExpression)
    elif (command == "get"):
        _checkLengthExpected("get", expr, 2)
        symbol = expr[1]
        if (not isinstance(symbol, Symbol)):
            raise ValueError('get argument must be a symbol.')
        return GetExpression(symbol)
    elif (command == "function"):
        _checkLengthExpected("function", expr, 5)
        functionType = solveType(expr)
        parameterSymbols = expr[3].value()
        parametersLength = len(parameterSymbols)
        if (parametersLength != len(functionType.parameterTypes)):
            raise ValueError('Function length of types and parameters do not match.')
        for i in range(parametersLength):
            symbol = parameterSymbols[i]
            if (not isinstance(symbol, Symbol)):
                raise ValueError('Each function parameter must be a symbol.')
        bodyExpression = parse(expr[4])
        return FunctionExpression(functionType, parameterSymbols, bodyExpression)
    elif (command == "apply"):
        _checkLengthExpected("apply", expr, 3)
        functionExpression = parse(expr[1])
        argumentExpressions = []
        for argumentExpression in expr[2].value():
            argumentExpressions.append(parse(argumentExpression))
        return ApplyExpression(functionExpression, argumentExpressions)
    else:
        raise ValueError('command ' + command + ' not defined.')
