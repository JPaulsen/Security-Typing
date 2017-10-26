from AST import *
from sexpdata import *
from Types import *


def _checkExpectedTypesOfValue(value, types):
    for type in types:
        if _isConsistentTypeOfValue(value, type):
            return
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def _isConsistentTypeOfValue(value, type):
    if isinstance(type, FunctionType):
        if not isinstance(value, FunctionExpression):
            return False
        return _areConsistentTypes(value.functionType, type)
    if isinstance(type, RefType):
        if not isinstance(value, RefExpression):
            return False
        return _areConsistentTypes(value.referencedType, type.referencedType)
    return isinstance(value, type)


def _areConsistentTypes(type1, type2):
    if isinstance(type1, FunctionType) and isinstance(type2, FunctionType):
        return _areConsistenFunctionTypes(type1, type2)
    if isinstance(type1, RefType) and isinstance(type2, RefType):
        return _areConsistentTypes(type1.referencedType, type2.referencedType)
    if isinstance(type1, FunctionType) or isinstance(type2, FunctionType) or isinstance(type1, RefType) or isinstance(
            type2, RefType):
        return False
    return type1 == type2


def _areConsistenFunctionTypes(functionType1, functionType2):
    parameterLength1 = len(functionType1.parameterTypes)
    parameterLength2 = len(functionType2.parameterTypes)
    if parameterLength1 != parameterLength2 or not _areConsistentTypes(functionType1.returnType,
                                                                       functionType2.returnType):
        return False
    for i in range(parameterLength1):
        if not _areConsistentTypes(functionType1.parameterTypes[i], functionType2.parameterTypes[i]):
            return False
    return True


def _checkExpectedTypes(type, types):
    for t in types:
        if _areConsistentTypes(type, t):
            return
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def typeCheck(ast):
    return ast.accept(TypeChecker())


class TypeChecker:
    def __init__(self):
        self.env = Environment()

    def visitBoolLiteral(self, boolLiteral):
        _checkExpectedTypesOfValue(boolLiteral.value, [bool])
        return bool

    def visitIntLiteral(self, intLiteral):
        _checkExpectedTypesOfValue(intLiteral.value, [int])
        return int

    def visitFloatLiteral(self, floatLiteral):
        _checkExpectedTypesOfValue(floatLiteral.value, [int, float])
        return float

    def visitStringLiteral(self, stringLiteral):
        _checkExpectedTypesOfValue(stringLiteral.value, [str])
        return str

    def visitUnaryExpression(self, unaryExpression):
        if unaryExpression.command == "not":
            _checkExpectedTypes(unaryExpression.expression.accept(self), [bool])
            return bool
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at typeChecker level.")

    def visitBinaryExpression(self, binaryExpression):
        if binaryExpression.command == "and" or binaryExpression.command == "or":
            _checkExpectedTypes(binaryExpression.firstExpression.accept(self), [bool])
            _checkExpectedTypes(binaryExpression.secondExpression.accept(self), [bool])
            return bool
        elif binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/":
            firstExpressionType = binaryExpression.firstExpression.accept(self)
            secondExpressionType = binaryExpression.secondExpression.accept(self)
            _checkExpectedTypes(firstExpressionType, [int, float])
            _checkExpectedTypes(secondExpressionType, [int, float])
            return float if firstExpressionType == float or secondExpressionType == float else int
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        _checkExpectedTypes(ifExpression.conditionExpression.accept(self), [bool])
        thenExpressionType = ifExpression.thenExpression.accept(self)
        elseExpressionType = ifExpression.elseExpression.accept(self)
        _checkExpectedTypes(elseExpressionType, [thenExpressionType])
        return thenExpressionType

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
        functionType = functionExpression.functionType
        parametersLength = len(functionType.parameterTypes)
        oldEnv = self.env
        self.env = Environment()
        for i in range(parametersLength):
            symbol = functionExpression.parameterSymbols[i]
            if not isinstance(symbol, Symbol):
                raise ValueError('Each function parameter must be a symbol.')
            self.env.put(functionExpression.parameterSymbols[i].value(), functionType.parameterTypes[i])
        bodyExpressionType = functionExpression.bodyExpression.accept(self)
        _checkExpectedTypes(bodyExpressionType, [functionType.returnType])
        self.env = oldEnv
        return functionType

    def visitApplyExpression(self, applyExpression):
        functionType = applyExpression.functionExpression.accept(self)
        argumentTypes = []
        for argument in applyExpression.argumentExpressions:
            argumentTypes.append(argument.accept(self))
        argumentsLength = len(argumentTypes)
        if len(functionType.parameterTypes) != argumentsLength:
            raise ValueError('Function length of parameters and arguments in apply do not match.')
        for i in range(argumentsLength):
            parameterType = functionType.parameterTypes[i]
            argumentType = argumentTypes[i]
            _checkExpectedTypes(argumentType, [parameterType])
        return functionType.returnType

    def visitRefExpression(self, refExpression):
        return RefType(refExpression.referencedType)

    def visitDerefExpression(self, derefExpression):
        refExpressionType = derefExpression.refExpression.accept(self)
        _checkExpectedTypesOfValue(refExpressionType, [RefType])
        return refExpressionType.referencedType

    def visitAssignmentExpression(self, assignmentExpression):
        refExpressionType = assignmentExpression.refExpression.accept(self)
        _checkExpectedTypesOfValue(refExpressionType, [RefType])
        valueExpressionType = assignmentExpression.valueExpression.accept(self)
        _checkExpectedTypes(valueExpressionType, [refExpressionType.referencedType])
        return assignmentExpression.bodyExpression.accept(self)
