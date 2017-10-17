from AST import *
from sexpdata import *
from Types import *


def checkExpectedTypesOfValue(value, types):
    for type in types:
        if _isConsistentTypeOfValue(value, type):
            return
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def _isConsistentTypeOfValue(value, type):
    if isinstance(type, DynamicType):
        return True
    if isinstance(type, FunctionType):
        if not isinstance(value, FunctionExpression):
            return False
        return _areConsistentTypes(value.functionType, type)
    return isinstance(value, type)


def _areConsistentTypes(type1, type2):
    if isinstance(type1, DynamicType) or isinstance(type2, DynamicType):
        return True
    if isinstance(type1, FunctionType) and isinstance(type2, FunctionType):
        return _areConsistenFunctionTypes(type1, type2)
    if isinstance(type1, FunctionType) or isinstance(type2, FunctionType):
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
        if _areConsistentTypes(t, type):
            return
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def typeCheck(ast):
    return ast.accept(TypeChecker())


class TypeChecker:
    def __init__(self):
        self.env = Environment()

    def visitBoolLiteral(self, boolLiteral):
        checkExpectedTypesOfValue(boolLiteral.value, [bool])
        return bool

    def visitIntLiteral(self, intLiteral):
        checkExpectedTypesOfValue(intLiteral.value, [int])
        return int

    def visitFloatLiteral(self, floatLiteral):
        checkExpectedTypesOfValue(floatLiteral.value, [int, float])
        return float

    def visitStringLiteral(self, stringLiteral):
        checkExpectedTypesOfValue(stringLiteral.value, [str])
        return str

    def visitDynamicLiteral(self, dynamicLiteral):
        checkExpectedTypesOfValue(dynamicLiteral.value, [bool, int, float, str])
        return DynamicType()

    def visitUnaryExpression(self, unaryExpression):
        if unaryExpression.command == "not":
            expressionType = unaryExpression.expression.accept(self)
            if isinstance(expressionType, DynamicType):
                unaryExpression.expression = CheckDynamicTypeExpression([bool], unaryExpression.expression)
            else:
                _checkExpectedTypes(expressionType, [bool])
            return bool
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at typeChecker level.")

    def visitBinaryExpression(self, binaryExpression):
        if binaryExpression.command == "and" or binaryExpression.command == "or":
            firstExpressionType = binaryExpression.firstExpression.accept(self)
            if isinstance(firstExpressionType, DynamicType):
                binaryExpression.firstExpression = CheckDynamicTypeExpression([bool], binaryExpression.firstExpression)
            else:
                _checkExpectedTypes(firstExpressionType, [bool])
            secondExpressionType = binaryExpression.secondExpression.accept(self)
            if isinstance(secondExpressionType, DynamicType):
                binaryExpression.secondExpression = CheckDynamicTypeExpression([bool],
                                                                               binaryExpression.secondExpression)
            else:
                _checkExpectedTypes(secondExpressionType, [bool])
            return bool
        elif binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/":
            firstExpressionType = binaryExpression.firstExpression.accept(self)
            if isinstance(firstExpressionType, DynamicType):
                binaryExpression.firstExpression = CheckDynamicTypeExpression([int, float],
                                                                              binaryExpression.firstExpression)
            else:
                _checkExpectedTypes(firstExpressionType, [int, float])
            secondExpressionType = binaryExpression.secondExpression.accept(self)
            if isinstance(secondExpressionType, DynamicType):
                binaryExpression.secondExpression = CheckDynamicTypeExpression([int, float],
                                                                               binaryExpression.secondExpression)
            else:
                _checkExpectedTypes(secondExpressionType, [int, float])

            return int if firstExpressionType == int and secondExpressionType == int else float
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        conditionExpressionType = ifExpression.conditionExpression.accept(self)
        if isinstance(conditionExpressionType, DynamicType):
            ifExpression.conditionExpression = CheckDynamicTypeExpression([bool], ifExpression.conditionExpression)
        else:
            _checkExpectedTypes(conditionExpressionType, [bool])
        thenExpressionType = ifExpression.thenExpression.accept(self)
        elseExpressionType = ifExpression.elseExpression.accept(self)
        if isinstance(thenExpressionType, DynamicType) or isinstance(elseExpressionType, DynamicType):
            return DynamicType()
        _checkExpectedTypes(thenExpressionType, [elseExpressionType])
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
        if not isinstance(functionType.returnType, DynamicType):
            if isinstance(bodyExpressionType, DynamicType):
                functionExpression.bodyExpression = CheckDynamicTypeExpression([functionType.returnType],
                                                                               functionExpression.bodyExpression)
            else:
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
            if not isinstance(parameterType, DynamicType):
                if isinstance(argumentType, DynamicType):
                    applyExpression.argumentExpressions[i] = CheckDynamicTypeExpression([parameterType],
                                                                                        applyExpression.argumentExpressions[
                                                                                            i])
                else:
                    _checkExpectedTypes(argumentType, [parameterType])
        return functionType.returnType

    def visitCheckDynamicTypeExpression(self, checkDynamicTypeExpression):
        return DynamicType()
