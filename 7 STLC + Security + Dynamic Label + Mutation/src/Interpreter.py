from TypeChecker import checkExpectedTypesOfValue
from AST import *
from Types import *


def interp(ast):
    return ast.accept(Interpreter())


class Interpreter:
    def __init__(self):
        self.env = Environment()
        self.store = Store()

    def visitBoolLiteral(self, boolLiteral):
        return SecurityValue(boolLiteral.value, boolLiteral.securityLabel)

    def visitIntLiteral(self, intLiteral):
        return SecurityValue(intLiteral.value, intLiteral.securityLabel)

    def visitFloatLiteral(self, floatLiteral):
        return SecurityValue(1.0 * floatLiteral.value, floatLiteral.securityLabel)

    def visitStringLiteral(self, stringLiteral):
        return SecurityValue(stringLiteral.value, stringLiteral.securityLabel)

    def visitUnaryExpression(self, unaryExpression):
        if (unaryExpression.command == "not"):
            return unaryExpression.expression.accept(self).boolNot()
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at interpreter level.")

    def visitBinaryExpression(self, binaryExpression):
        if binaryExpression.command == "and":
            return binaryExpression.firstExpression.accept(self).boolAnd(binaryExpression.secondExpression.accept(self))
        elif binaryExpression.command == "or":
            return binaryExpression.firstExpression.accept(self).boolOr(binaryExpression.secondExpression.accept(self))
        elif binaryExpression.command == "+":
            return binaryExpression.firstExpression.accept(self) + binaryExpression.secondExpression.accept(self)
        elif binaryExpression.command == "-":
            return binaryExpression.firstExpression.accept(self) - binaryExpression.secondExpression.accept(self)
        elif binaryExpression.command == "*":
            return binaryExpression.firstExpression.accept(self) * binaryExpression.secondExpression.accept(self)
        elif binaryExpression.command == "/":
            return binaryExpression.firstExpression.accept(self) / binaryExpression.secondExpression.accept(self)
        raise ValueError("BinaryExpression with command " + binaryExpression.command + " not yet implemented.")

    def visitIfExpression(self, ifExpression):
        if ifExpression.conditionExpression.accept(self):
            return ifExpression.thenExpression.accept(self)
        else:
            return ifExpression.elseExpression.accept(self)

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
        return SecurityValue(functionExpression, functionExpression.securityType.securityLabel)

    def visitApplyExpression(self, applyExpression):
        functionExpression = applyExpression.functionExpression.accept(self).value
        arguments = []
        for argument in applyExpression.argumentExpressions:
            arguments.append(argument.accept(self))
        oldEnv = self.env
        self.env = Environment()
        argumentsLength = len(arguments)
        for i in range(argumentsLength):
            checkExpectedTypesOfValue(arguments[i], [functionExpression.securityType.type.parameterTypes[i]])
            self.env.put(functionExpression.parameterSymbols[i].value(), arguments[i])
        ans = functionExpression.bodyExpression.accept(self)
        self.env = oldEnv
        checkExpectedTypesOfValue(ans, [functionExpression.securityType.type.returnType])
        return ans

    def visitCheckDynamicTypeExpression(self, checkDynamicTypeExpression):
        value = checkDynamicTypeExpression.expression.accept(self)
        checkExpectedTypesOfValue(value, checkDynamicTypeExpression.types)
        return value

    def visitRefExpression(self, refExpression):
        return SecurityValue(self.store.createRef(), refExpression.referencedSecurityType.securityLabel)

    def visitDerefExpression(self, derefExpression):
        return self.store.get(derefExpression.refExpression.accept(self).value)

    def visitAssignmentExpression(self, assignmentExpression):
        key = assignmentExpression.refExpression.accept(self)
        value = assignmentExpression.valueExpression.accept(self)
        self.store.put(key.value, value)
        return assignmentExpression.bodyExpression.accept(self)
