from AST import *
from TypeParser import *
from sexpdata import *


def _checkLengthExpected(name, expr, n):
    if len(expr) != n:
        lastPart = ' elements.'
        if (n == 1):
            lastPart = ' element.'
        raise ValueError(name + ' expressions must have ' + str(n) + lastPart)


def parse(expr):
    if len(expr) == 0:
        raise ValueError('expressions can not be empty.')
    command = expr[0]
    if not isinstance(command, Symbol):
        raise ValueError('first keyword of a expression must be a symbol.')
    command = command.value()
    if command == 'bool':
        _checkLengthExpected("Boolean literal", expr, 3)
        securityLabel = SecurityLabel(expr[1].value())
        if (securityLabel.isDynamicLabel()):
            raise ValueError('Literals can not have dynamic labels.')
        value = expr[2]
        return BoolLiteral(securityLabel, value)
    elif command == 'int':
        _checkLengthExpected("Integer literal", expr, 3)
        securityLabel = SecurityLabel(expr[1].value())
        if (securityLabel.isDynamicLabel()):
            raise ValueError('Literals can not have dynamic labels.')
        value = expr[2]
        return IntLiteral(securityLabel, value)
    elif command == 'float':
        _checkLengthExpected("Float literal", expr, 3)
        securityLabel = SecurityLabel(expr[1].value())
        if (securityLabel.isDynamicLabel()):
            raise ValueError('Literals can not have dynamic labels.')
        value = expr[2]
        return FloatLiteral(securityLabel, value)
    elif command == 'str':
        _checkLengthExpected("String literal", expr, 3)
        securityLabel = SecurityLabel(expr[1].value())
        if (securityLabel.isDynamicLabel()):
            raise ValueError('Literals can not have dynamic labels.')
        value = expr[2]
        return StringLiteral(securityLabel, value)
    elif command == "not":
        _checkLengthExpected("not", expr, 2)
        expression = parse(expr[1])
        return UnaryExpression("not", expression)
    elif command == "and" or command == "or" or command == "+" or command == "-" or command == "*" or command == "/":
        _checkLengthExpected(command, expr, 3)
        firstExpression = parse(expr[1])
        secondExpression = parse(expr[2])
        return BinaryExpression(command, firstExpression, secondExpression)
    elif command == "if":
        _checkLengthExpected("if", expr, 4)
        conditionExpression = parse(expr[1])
        thenExpression = parse(expr[2])
        elseExpression = parse(expr[3])
        return IfExpression(conditionExpression, thenExpression, elseExpression)
    elif command == "let":
        _checkLengthExpected("let", expr, 4)
        symbol = expr[1]
        if not isinstance(symbol, Symbol):
            raise ValueError('let first argument must be a symbol.')
        valueExpression = parse(expr[2])
        thenExpression = parse(expr[3])
        return LetExpression(symbol, valueExpression, thenExpression)
    elif command == "function":
        _checkLengthExpected("function", expr, 5)
        securityType = parseFunctionSecurityType(expr)
        if (securityType.securityLabel.isDynamicLabel()):
            raise ValueError('Literals can not have dynamic labels.')
        parameterSymbols = map(_getSecond, expr[3].value())
        parametersLength = len(parameterSymbols)
        if parametersLength != len(securityType.type.parameterTypes):
            raise ValueError('Function length of types and parameters do not match.')
        for i in range(parametersLength):
            symbol = parameterSymbols[i]
            if not isinstance(symbol, Symbol):
                raise ValueError('Each function parameter must be a symbol.')
        bodyExpression = parse(expr[4])
        return FunctionExpression(securityType, parameterSymbols, bodyExpression)
    elif command == "apply":
        _checkLengthExpected("apply", expr, 3)
        functionExpression = parse(expr[1])
        argumentExpressions = []
        for argumentExpression in expr[2].value():
            argumentExpressions.append(parse(argumentExpression))
        return ApplyExpression(functionExpression, argumentExpressions)
    elif command == "ref":
        checkLengthExpected("ref", expr, 2)
        return RefExpression(parseSecurityType(expr[1]))
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
