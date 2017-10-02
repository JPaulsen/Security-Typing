from AST import *
from TypeChecker import checkExpectedTypesOfValue

def interp(ast):
    return ast.accept(Interpreter())


class Interpreter:
    def __init__(self):
        self.env = Environment()

    def visitBoolLiteral(self, boolLiteral):
        return boolLiteral.value

    def visitIntLiteral(self, intLiteral):
        return intLiteral.value

    def visitFloatLiteral(self, floatLiteral):
        return 1.0 * floatLiteral.value

    def visitStringLiteral(self, stringLiteral):
        return stringLiteral.value

    def visitDynamicLiteral(self, dynamicLiteral):
        return dynamicLiteral.value

    def visitUnaryExpression(self, unaryExpression):
        if unaryExpression.command == "not":
            return not unaryExpression.expression.accept(self)
        raise ValueError(
            "UnaryExpression with command " + unaryExpression.command + " not yet implemented at interpreter level.")

    def visitBinaryExpression(self, binaryExpression):
        if binaryExpression.command == "and":
            return binaryExpression.firstExpression.accept(self) and binaryExpression.secondExpression.accept(self)
        elif binaryExpression.command == "or":
            return binaryExpression.firstExpression.accept(self) or binaryExpression.secondExpression.accept(self)
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
        return functionExpression

    def visitApplyExpression(self, applyExpression):
        functionExpression = applyExpression.functionExpression.accept(self)
        arguments = []
        for argument in applyExpression.argumentExpressions:
            arguments.append(argument.accept(self))
        oldEnv = self.env
        self.env = Environment()
        argumentsLength = len(arguments)
        for i in range(argumentsLength):
            self.env.put(functionExpression.parameterSymbols[i].value(), arguments[i])
        ans = functionExpression.bodyExpression.accept(self)
        self.env = oldEnv
        return ans

    def visitCheckDynamicTypeExpression(self, checkDynamicTypeExpression):
        value = checkDynamicTypeExpression.expression.accept(self)
        checkExpectedTypesOfValue(value, checkDynamicTypeExpression.types)
        return value
