from AST import *
from Types import *
from sexpdata import *


def checkExpectedTypesOfValue(value, types):
    for type in types:
        if _isConsistentTypeOfValue(value, type):
            return
    raise ValueError(' or '.join(map(str, types)) + ' was expected.')


def _isConsistentTypeOfValue(value, type):
    if isinstance(type, FunctionType):
        if not isinstance(value, FunctionExpression):
            return False
        return _areConsistentTypes(value.securityType.type, type)
    if isinstance(type, SecurityType):
        if not isinstance(value, SecurityValue):
            return False
        return value.securityLabel <= type.securityLabel and _isConsistentTypeOfValue(value.value, type.type)
    return isinstance(value, type)


def _areConsistentTypes(type1, type2):
    if isinstance(type1, FunctionType) and isinstance(type2, FunctionType):
        return _areConsistenFunctionTypes(type1, type2)
    if isinstance(type1, SecurityType) and isinstance(type2, SecurityType):
        return type1.securityLabel <= type2.securityLabel and _areConsistentTypes(type1.type, type2.type)
    if isinstance(type1, FunctionType) or isinstance(type2, FunctionType) or isinstance(type1,
                                                                                        SecurityType) or isinstance(
        type2, SecurityType):
        return False
    return type1 == type2


def _areConsistenFunctionTypes(functionType1, functionType2):
    parameterLength1 = len(functionType1.parameterTypes)
    parameterLength2 = len(functionType2.parameterTypes)
    if parameterLength1 != parameterLength2 or not _areConsistentTypes(functionType2.returnType,
                                                                       functionType1.returnType):
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
        self.pc = SecurityLabel("b")

    def visitBoolLiteral(self, boolLiteral):
        checkExpectedTypesOfValue(boolLiteral.value, [bool])
        return TypeCheckerResult(SecurityType(bool, boolLiteral.securityLabel), boolLiteral)

    def visitIntLiteral(self, intLiteral):
        checkExpectedTypesOfValue(intLiteral.value, [int])
        return TypeCheckerResult(SecurityType(int, intLiteral.securityLabel), intLiteral)

    def visitFloatLiteral(self, floatLiteral):
        checkExpectedTypesOfValue(floatLiteral.value, [int, float])
        return TypeCheckerResult(SecurityType(float, floatLiteral.securityLabel), floatLiteral)

    def visitStringLiteral(self, stringLiteral):
        checkExpectedTypesOfValue(stringLiteral.value, [str])
        return TypeCheckerResult(SecurityType(str, stringLiteral.securityLabel), stringLiteral)

    def visitUnaryExpression(self, unaryExpression):
        if unaryExpression.command == "not":
            expressionTypeCheckerResult = unaryExpression.expression.accept(self)
            unaryExpression.expression = expressionTypeCheckerResult.astNode
            expressionType = expressionTypeCheckerResult.type
            _checkExpectedTypes(expressionType.type, [bool])
            return TypeCheckerResult(expressionType, unaryExpression)
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at typeChecker level.")

    def visitBinaryExpression(self, binaryExpression):
        firstExpressionTypeCheckerResult = binaryExpression.firstExpression.accept(self)
        binaryExpression.firstExpression = firstExpressionTypeCheckerResult.astNode
        firstExpressionType = firstExpressionTypeCheckerResult.type
        secondExpressionTypeCheckerResult = binaryExpression.secondExpression.accept(self)
        binaryExpression.secondExpression = secondExpressionTypeCheckerResult.astNode
        secondExpressionType = secondExpressionTypeCheckerResult.type
        securityLabel = SecurityLabel.join(firstExpressionType.securityLabel, secondExpressionType.securityLabel)
        if binaryExpression.command == "and" or binaryExpression.command == "or":
            _checkExpectedTypes(firstExpressionType.type, [bool])
            _checkExpectedTypes(secondExpressionType.type, [bool])
            return TypeCheckerResult(SecurityType(bool, securityLabel), binaryExpression)
        elif binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/":
            _checkExpectedTypes(firstExpressionType.type, [int, float])
            _checkExpectedTypes(secondExpressionType.type, [int, float])
            type = float if firstExpressionType.type == float or secondExpressionType.type == float else int
            return TypeCheckerResult(SecurityType(type, securityLabel), binaryExpression)
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        conditionExpressionTypeCheckerResult = ifExpression.conditionExpression.accept(self)
        ifExpression.conditionExpression = conditionExpressionTypeCheckerResult.astNode
        conditionExpressionType = conditionExpressionTypeCheckerResult.type
        _checkExpectedTypes(conditionExpressionType.type, [bool])
        oldPc = self.pc
        self.pc = SecurityLabel.join(self.pc, conditionExpressionType.securityLabel)
        thenExpressionTypeCheckerResult = ifExpression.thenExpression.accept(self)
        ifExpression.thenExpression = thenExpressionTypeCheckerResult.astNode
        thenExpressionType = thenExpressionTypeCheckerResult.type
        elseExpressionTypeCheckerResult = ifExpression.elseExpression.accept(self)
        ifExpression.elseExpression = elseExpressionTypeCheckerResult.astNode
        elseExpressionType = elseExpressionTypeCheckerResult.type
        self.pc = oldPc
        _checkExpectedTypes(elseExpressionType.type, [thenExpressionType.type])
        return TypeCheckerResult(SecurityType(thenExpressionType.type, SecurityLabel.joinMultiple(
            [conditionExpressionType.securityLabel, thenExpressionType.securityLabel,
             elseExpressionType.securityLabel])), ifExpression)

    def visitLetExpression(self, letExpression):
        oldEnv = self.env
        self.env = self.env.clone()
        valueExpressionTypeCheckerResult = letExpression.valueExpression.accept(self)
        letExpression.valueExpression = valueExpressionTypeCheckerResult.astNode
        valueExpressionType = valueExpressionTypeCheckerResult.type
        self.env.put(letExpression.symbol.value(), valueExpressionType)
        thenExpressionTypeCheckerResult = letExpression.thenExpression.accept(self)
        letExpression.thenExpression = thenExpressionTypeCheckerResult.astNode
        thenExpressionType = thenExpressionTypeCheckerResult.type
        self.env = oldEnv
        return TypeCheckerResult(thenExpressionType, letExpression)

    def visitGetExpression(self, getExpression):
        return TypeCheckerResult(self.env.get(getExpression.symbol.value()), getExpression)

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
        oldPc = self.pc
        self.pc = securityType.securityLabel
        bodyExpressionTypeCheckerResult = functionExpression.bodyExpression.accept(self)
        functionExpression.bodyExpression = bodyExpressionTypeCheckerResult.astNode
        bodyExpressionType = bodyExpressionTypeCheckerResult.type
        self.pc = oldPc
        _checkExpectedTypes(bodyExpressionType, [securityType.type.returnType])
        if not securityType.type.returnType.securityLabel.isDynamicLabel() and bodyExpressionType.securityLabel.isDynamicLabel():
            functionExpression.bodyExpression = CheckDynamicTypeExpression([securityType.type.returnType],
                                                                           functionExpression.bodyExpression)
        self.env = oldEnv
        return TypeCheckerResult(securityType, functionExpression)

    def visitApplyExpression(self, applyExpression):
        functionExpressionTypeCheckerResult = applyExpression.functionExpression.accept(self)
        applyExpression.functionExpression = functionExpressionTypeCheckerResult.astNode
        securityType = functionExpressionTypeCheckerResult.type
        argumentTypes = []
        for i in range(len(applyExpression.argumentExpressions)):
            argumentTypeCheckerResult = applyExpression.argumentExpressions[i].accept(self)
            applyExpression.argumentExpressions[i] = argumentTypeCheckerResult.astNode
            argumentType = argumentTypeCheckerResult.type
            argumentTypes.append(argumentType)
        argumentsLength = len(argumentTypes)
        if len(securityType.type.parameterTypes) != argumentsLength:
            raise ValueError('Function length of parameters and arguments in apply do not match.')
        for i in range(argumentsLength):
            parameterType = securityType.type.parameterTypes[i]
            argumentType = argumentTypes[i]
            _checkExpectedTypes(argumentType, [parameterType])
        if not securityType.securityLabel >= self.pc:
            raise ValueError(
                "Application of a " + str(securityType.securityLabel) + " function in a " + str(self.pc) + " context.")
        return TypeCheckerResult(securityType.type.returnType,
                                 CheckDynamicTypeExpression([securityType.type.returnType], applyExpression))

    def visitRefExpression(self, refExpression):
        return TypeCheckerResult(RefType(refExpression.referencedSecurityType), refExpression)

    def visitDerefExpression(self, derefExpression):
        refExpressionTypeCheckerResult = derefExpression.refExpression.accept(self)
        derefExpression.refExpression = refExpressionTypeCheckerResult.astNode
        refExpressionType = refExpressionTypeCheckerResult.type
        checkExpectedTypesOfValue(refExpressionType, [RefType])
        return TypeCheckerResult(refExpressionType.referencedSecurityType, derefExpression)

    def visitAssignmentExpression(self, assignmentExpression):
        refExpressionTypeCheckerResult = assignmentExpression.refExpression.accept(self)
        assignmentExpression.refExpression = refExpressionTypeCheckerResult.astNode
        refExpressionType = refExpressionTypeCheckerResult.type
        checkExpectedTypesOfValue(refExpressionType, [RefType])
        valueExpressionTypeCheckerResult = assignmentExpression.valueExpression.accept(self)
        assignmentExpression.valueExpression = valueExpressionTypeCheckerResult.astNode
        valueExpressionType = valueExpressionTypeCheckerResult.type
        _checkExpectedTypes(valueExpressionType, [refExpressionType.referencedSecurityType])
        if not refExpressionType.securityLabel >= self.pc:
            raise ValueError(str(refExpressionType.securityLabel) + " assignation in a " + str(self.pc) + " context.")
        bodyExpressionTypeCheckerResult = assignmentExpression.bodyExpression.accept(self)
        assignmentExpression.bodyExpression = bodyExpressionTypeCheckerResult.astNode
        return TypeCheckerResult(bodyExpressionTypeCheckerResult.type, assignmentExpression)


class TypeCheckerResult:
    def __init__(self, type, astNode):
        self.type = type
        self.astNode = astNode
