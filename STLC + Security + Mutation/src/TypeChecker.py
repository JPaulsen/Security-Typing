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
        if type <= t:
            return;
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def typeCheck(ast):
    return ast.accept(TypeChecker())


class TypeChecker:
    def __init__(self):
        self.env = Environment()
        self.pc = SecurityLabel("b")

    def visitBoolLiteral(self, boolLiteral):
        _checkExpectedTypesOfValue(boolLiteral.value, [bool])
        return SecurityType(bool, boolLiteral.securityLabel)

    def visitIntLiteral(self, intLiteral):
        _checkExpectedTypesOfValue(intLiteral.value, [int])
        return SecurityType(int, intLiteral.securityLabel)

    def visitFloatLiteral(self, floatLiteral):
        _checkExpectedTypesOfValue(floatLiteral.value, [int, float])
        return SecurityType(float, floatLiteral.securityLabel)

    def visitStringLiteral(self, stringLiteral):
        _checkExpectedTypesOfValue(stringLiteral.value, [str])
        return SecurityType(str, stringLiteral.securityLabel)

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
        securityLabel = SecurityLabel.join(firstExpressionType.securityLabel, secondExpressionType.securityLabel)
        if binaryExpression.command == "and" or binaryExpression.command == "or":
            _checkExpectedTypes(firstExpressionType.type, [bool])
            _checkExpectedTypes(secondExpressionType.type, [bool])
            return SecurityType(bool, securityLabel)
        elif binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/":
            _checkExpectedTypes(firstExpressionType.type, [int, float])
            _checkExpectedTypes(secondExpressionType.type, [int, float])
            type = float if firstExpressionType.type == float or secondExpressionType.type == float else int
            return SecurityType(type, securityLabel)
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        condExpressionType = ifExpression.conditionExpression.accept(self)
        _checkExpectedTypes(condExpressionType.type, [bool])
        oldPc = self.pc
        self.pc = SecurityLabel.join(self.pc, condExpressionType.securityLabel)
        thenExpressionType = ifExpression.thenExpression.accept(self)
        elseExpressionType = ifExpression.elseExpression.accept(self)
        self.pc = oldPc
        _checkExpectedTypes(elseExpressionType.type, [thenExpressionType.type])
        return SecurityType(thenExpressionType.type, SecurityLabel.joinMultiple(
            [condExpressionType.securityLabel, thenExpressionType.securityLabel, elseExpressionType.securityLabel]))

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
        securityType = functionExpression.securityType
        parametersLength = len(securityType.type.parameterTypes)
        oldEnv = self.env
        self.env = Environment()
        for i in range(parametersLength):
            symbol = functionExpression.parameterSymbols[i]
            if not isinstance(symbol, Symbol):
                raise ValueError('Each function parameter must be a symbol.')
            self.env.put(functionExpression.parameterSymbols[i].value(), securityType.type.parameterTypes[i])
        bodyExpressionType = functionExpression.bodyExpression.accept(self)
        if securityType.type.returnType.type != bodyExpressionType.type:
            raise ValueError('Body return type does not match Function return type.')
        if securityType.type.returnType.securityLabel < bodyExpressionType.securityLabel:
            raise ValueError('Body return security type is higher than Function return security type.')
        self.env = oldEnv
        return securityType

    def visitApplyExpression(self, applyExpression):
        securityType = applyExpression.functionExpression.accept(self)
        argumentTypes = []
        for argument in applyExpression.argumentExpressions:
            argumentTypes.append(argument.accept(self))
        argumentsLength = len(argumentTypes)
        if len(securityType.type.parameterTypes) != argumentsLength:
            raise ValueError('Function length of parameters and arguments in apply do not match.')
        for i in range(argumentsLength):
            parameterType = securityType.type.parameterTypes[i]
            argumentType = argumentTypes[i]
            _checkExpectedTypes(argumentType.type, [parameterType.type])
            if parameterType.securityLabel < argumentType.securityLabel:
                raise ValueError('Argument security type is higher than Function parameter security type.')
        return securityType.type.returnType

    def visitRefExpression(self, refExpression):
        return RefType(refExpression.referencedSecurityType)

    def visitDerefExpression(self, derefExpression):
        refExpressionType = derefExpression.refExpression.accept(self)
        _checkExpectedTypesOfValue(refExpressionType, [RefType])
        return refExpressionType.referencedType

    def visitAssignmentExpression(self, assignmentExpression):
        refExpressionType = assignmentExpression.refExpression.accept(self)
        _checkExpectedTypesOfValue(refExpressionType, [RefType])
        valueExpressionType = assignmentExpression.valueExpression.accept(self)
        _checkExpectedTypes(valueExpressionType, [refExpressionType.referencedSecurityType])
        if (refExpressionType.securityLabel < self.pc):
            raise ValueError(str(refExpressionType.securityLabel) + " assignation in a " + str(self.pc) + " context.")
        return assignmentExpression.bodyExpression.accept(self)
