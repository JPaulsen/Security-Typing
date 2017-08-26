from AST import *
from Types import *
from sexpdata import *


def _checkExpectedTypesOfValue(value, types):
    for type in types:
        if isinstance(value, type):
            return;
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def _checkExpectedTypes(type, types):
    for t in types:
        if type == t:
            return;
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def typeCheck(ast):
    return ast.accept(TypeChecker())


class TypeChecker:
    def __init__(self):
        self.env = Environment()

    def visitBoolLiteral(self, boolLiteral):
        _checkExpectedTypesOfValue(boolLiteral.value, [bool])
        return PairType(bool, boolLiteral.securityType)

    def visitIntLiteral(self, intLiteral):
        _checkExpectedTypesOfValue(intLiteral.value, [int])
        return PairType(int, intLiteral.securityType)

    def visitFloatLiteral(self, floatLiteral):
        _checkExpectedTypesOfValue(floatLiteral.value, [int, float])
        return PairType(float, floatLiteral.securityType)

    def visitStringLiteral(self, stringLiteral):
        _checkExpectedTypesOfValue(stringLiteral.value, [str])
        return PairType(str, stringLiteral.securityType)

    def visitUnaryExpression(self, unaryExpression):
        if unaryExpression.command == "not":
            expressionType = unaryExpression.expression.accept(self)
            _checkExpectedTypes(expressionType.type, [bool])
            return expressionType
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at typeChecker level.")

    def visitBinaryExpression(self, binaryExpression):
        firstExpressionType = binaryExpression.firstExpression.accept(self)
        secondExpressionType = binaryExpression.secondExpression.accept(self)
        securityType = SecurityType.join(firstExpressionType.securityType, secondExpressionType.securityType)
        if binaryExpression.command == "and" or binaryExpression.command == "or":
            _checkExpectedTypes(firstExpressionType.type, [bool])
            _checkExpectedTypes(secondExpressionType.type, [bool])
            return PairType(bool, securityType)
        elif binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/":
            _checkExpectedTypes(firstExpressionType.type, [int, float])
            _checkExpectedTypes(secondExpressionType.type, [int, float])
            type = float if firstExpressionType.type == float or secondExpressionType.type == float else int
            return PairType(type, securityType)
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        condExpressionType = ifExpression.conditionExpression.accept(self)
        _checkExpectedTypes(condExpressionType.type, [bool])
        thenExpressionType = ifExpression.thenExpression.accept(self)
        elseExpressionType = ifExpression.elseExpression.accept(self)
        _checkExpectedTypes(elseExpressionType.type, [thenExpressionType.type])
        return PairType(thenExpressionType.type, SecurityType.joinMultiple(
            [condExpressionType.securityType, thenExpressionType.securityType, elseExpressionType.securityType]))

    def visitLetExpression(self, letExpression):
        oldEnv = self.env
        self.env = self.env.clone()
        self.env.put(letExpression.symbol.value(), letExpression.valueExpression.accept(self))
        ans = letExpression.thenExpression.accept(self)
        self.env = oldEnv
        return ans

    def visitGetExpression(self, getExpression):
        return self.env.get(getExpression.symbol.value())

    def visitFunctionExpression(self, functionExpression):
        pairType = functionExpression.pairType
        parametersLength = len(pairType.type.parameterTypes)
        oldEnv = self.env
        self.env = Environment()
        for i in range(parametersLength):
            symbol = functionExpression.parameterSymbols[i]
            if not isinstance(symbol, Symbol):
                raise ValueError('Each function parameter must be a symbol.')
            self.env.put(functionExpression.parameterSymbols[i].value(), pairType.type.parameterTypes[i])
        bodyExpressionType = functionExpression.bodyExpression.accept(self)
        if pairType.type.returnType.type != bodyExpressionType.type:
            raise ValueError('Body return type does not match Function return type.')
        if pairType.type.returnType.securityType < bodyExpressionType.securityType:
            raise ValueError('Body return security type is higher than Function return security type.')
        self.env = oldEnv
        return pairType

    def visitApplyExpression(self, applyExpression):
        pairType = applyExpression.functionExpression.accept(self)
        argumentTypes = []
        for argument in applyExpression.argumentExpressions:
            argumentTypes.append(argument.accept(self))
        argumentsLength = len(argumentTypes)
        if len(pairType.type.parameterTypes) != argumentsLength:
            raise ValueError('Function length of parameters and arguments in apply do not match.')
        for i in range(argumentsLength):
            parameterType = pairType.type.parameterTypes[i]
            argumentType = argumentTypes[i]
            _checkExpectedTypes(argumentType.type, [parameterType.type])
            if parameterType.securityType < argumentType.securityType:
                raise ValueError('Argument security type is higher than Function parameter security type.')
        return pairType.type.returnType
