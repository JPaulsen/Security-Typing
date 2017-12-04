class BoolLiteral:
    def __init__(self, securityLabel, value):
        self.securityLabel = securityLabel
        self.value = value

    def accept(self, visitor):
        return visitor.visitBoolLiteral(self)

    def __str__(self):
        return "(bool " + str(self.value) + ")"


class IntLiteral:
    def __init__(self, securityLabel, value):
        self.securityLabel = securityLabel
        self.value = value

    def accept(self, visitor):
        return visitor.visitIntLiteral(self)

    def __str__(self):
        return "(int " + str(self.value) + ")"


class FloatLiteral:
    def __init__(self, securityLabel, value):
        self.securityLabel = securityLabel
        self.value = value

    def accept(self, visitor):
        return visitor.visitFloatLiteral(self)

    def __str__(self):
        return "(float " + str(self.value) + ")"


class StringLiteral:
    def __init__(self, securityLabel, value):
        self.securityLabel = securityLabel
        self.value = value

    def accept(self, visitor):
        return visitor.visitStringLiteral(self)

    def __str__(self):
        return "(str " + str(self.value) + ")"


class UnaryExpression:
    def __init__(self, command, expression):
        self.command = command
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)

    def __str__(self):
        return "(" + self.command + " " + str(self.expression) + ")"


class BinaryExpression:
    def __init__(self, command, firstExpression, secondExpression):
        self.command = command
        self.firstExpression = firstExpression
        self.secondExpression = secondExpression

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)

    def __str__(self):
        return "(" + self.command + " " + str(self.firstExpression) + " " + str(self.secondExpression) + ")"


class IfExpression:
    def __init__(self, conditionExpression, thenExpression, elseExpression):
        self.conditionExpression = conditionExpression
        self.thenExpression = thenExpression
        self.elseExpression = elseExpression

    def accept(self, visitor):
        return visitor.visitIfExpression(self)

    def __str__(self):
        return "(if " + str(self.conditionExpression) + " " + str(self.thenExpression) + " " + str(
            self.elseExpression) + ")"


class LetExpression:
    def __init__(self, symbol, valueExpression, thenExpression):
        self.symbol = symbol
        self.valueExpression = valueExpression
        self.thenExpression = thenExpression

    def accept(self, visitor):
        return visitor.visitLetExpression(self)

    def __str__(self):
        return "(let " + str(self.symbol) + " " + str(self.valueExpression) + " " + str(self.thenExpression) + ")"


class GetExpression:
    def __init__(self, symbol):
        self.symbol = symbol

    def accept(self, visitor):
        return visitor.visitGetExpression(self)

    def __str__(self):
        return "(get " + str(self.symbol) + ")"


class FunctionExpression:
    def __init__(self, securityType, parameterSymbols, bodyExpression):
        self.securityType = securityType
        self.parameterSymbols = parameterSymbols
        self.bodyExpression = bodyExpression

    def accept(self, visitor):
        return visitor.visitFunctionExpression(self)

    def __str__(self):
        return str(self.securityType) + " [" + ", ".join(map(str, self.parameterSymbols)) + "] " + str(
            self.bodyExpression)


class ApplyExpression:
    def __init__(self, functionExpression, argumentExpressions):
        self.functionExpression = functionExpression
        self.argumentExpressions = argumentExpressions

    def accept(self, visitor):
        return visitor.visitApplyExpression(self)

    def __str__(self):
        return "(apply " + str(self.functionExpression) + " " + ", ".join(map(str, self.argumentExpressions)) + ")"


class RefExpression:
    def __init__(self, referencedSecurityType):
        self.referencedSecurityType = referencedSecurityType

    def accept(self, visitor):
        return visitor.visitRefExpression(self)

    def __str__(self):
        return "(ref " + str(self.referencedSecurityType) + ")"


class DerefExpression:
    def __init__(self, refExpression):
        self.refExpression = refExpression

    def accept(self, visitor):
        return visitor.visitDerefExpression(self)

    def __str__(self):
        return "(deref " + str(self.refExpression) + ")"


class AssignmentExpression:
    def __init__(self, refExpression, valueExpression, bodyExpression):
        self.refExpression = refExpression
        self.valueExpression = valueExpression
        self.bodyExpression = bodyExpression

    def accept(self, visitor):
        return visitor.visitAssignmentExpression(self)

    def __str__(self):
        return "(assign " + str(self.refExpression) + ", " + str(self.valueExpression) + ", " + str(
            self.bodyExpression) + ")"


class CheckDynamicTypeExpression:
    def __init__(self, types, expression):
        self.types = types
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitCheckDynamicTypeExpression(self)

    def __str__(self):
        return "(check [" + ", ".join(map(str, self.types)) + "] " + str(self.expression) + ")"


class Environment:
    def __init__(self):
        self.dictionary = {}

    def put(self, key, value):
        self.dictionary[key] = value

    def get(self, key):
        try:
            return self.dictionary[key]
        except:
            raise ValueError(key + ' was not declared in this scope.')

    def clone(self):
        newEnv = Environment()
        newEnv.dictionary = self.dictionary.copy()
        return newEnv


class Store:
    def __init__(self):
        self.dictionary = {}
        self.size = 0

    def put(self, key, value):
        if key >= self.size:
            raise ValueError('Memory slot not available.')
        if not isinstance(key, int):
            raise ValueError('Store keys must be an integer.')
        self.dictionary[key] = value

    def get(self, key):
        if key >= self.size:
            raise ValueError('Memory slot not available.')
        if not isinstance(key, int):
            raise ValueError('Store keys must be an integer.')
        try:
            return self.dictionary[key]
        except:
            raise ValueError('NullPointerException.')

    def createRef(self):
        self.size += 1
        return self.size - 1
