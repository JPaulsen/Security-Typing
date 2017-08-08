from sexpdata import *

class Expression:
	def __init__(self, expressionType):
		self.expressionType = expressionType

	def __str__(self):
		return str(self.expressionType)

class BoolLiteral(Expression, object):
	def __init__(self, value):
		super(self.__class__, self).__init__(bool)
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitBoolLiteral(self, env)

class IntLiteral(Expression, object):
	def __init__(self, value):
		super(self.__class__, self).__init__(int)
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitIntLiteral(self, env)

class FloatLiteral(Expression, object):
	def __init__(self, value):
		super(self.__class__, self).__init__(float)
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitFloatLiteral(self, env)

class StringLiteral(Expression, object):
	def __init__(self, value):
		super(self.__class__, self).__init__(str)
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitStringLiteral(self, env)

class UnaryExpression(Expression, object):
	def __init__(self, type, command, expression):
		super(self.__class__, self).__init__(type)
		self.command = command
		self.expression = expression

	def accept(self, visitor, env):
		return visitor.visitUnaryExpression(self, env)

class BinaryExpression(Expression, object):
	def __init__(self, type, command, firstExpression, secondExpression):
		super(self.__class__, self).__init__(type)
		self.command = command
		self.firstExpression = firstExpression
		self.secondExpression = secondExpression

	def accept(self, visitor, env):
		return visitor.visitBinaryExpression(self, env)

class IfExpression(Expression, object):
	def __init__(self, conditionExpression, thenExpression, elseExpression):
		super(self.__class__, self).__init__(thenExpression.expressionType)
		self.conditionExpression = conditionExpression
		self.thenExpression = thenExpression
		self.elseExpression = elseExpression

	def accept(self, visitor, env):
		return visitor.visitIfExpression(self, env)

class SetExpression(Expression, object):
	def __init__(self, symbol, valueExpression, thenExpression):
		super(self.__class__, self).__init__(thenExpression.expressionType)
		self.symbol = symbol
		self.valueExpression = valueExpression
		self.thenExpression = thenExpression

	def accept(self, visitor, env):
		return visitor.visitSetExpression(self, env)

class GetExpression(Expression, object):
	def __init__(self, type, symbol):
		super(self.__class__, self).__init__(type)
		self.symbol = symbol

	def accept(self, visitor, env):
		return visitor.visitGetExpression(self, env)

class FunctionExpression(Expression, object):
	def __init__(self, functionType, parameterSymbols, bodyExpression):
		super(self.__class__, self).__init__(functionType)
		self.parameterSymbols = parameterSymbols
		self.bodyExpression = bodyExpression

	def accept(self, visitor, env):
		return visitor.visitFunctionExpression(self, env)

class ApplyExpression(Expression, object):
	def __init__(self, functionExpression, argumentExpressions):
		super(self.__class__, self).__init__(functionExpression.expressionType.returnType)
		self.functionExpression = functionExpression
		self.argumentExpressions = argumentExpressions

	def accept(self, visitor, env):
		return visitor.visitApplyExpression(self, env)

class FunctionType:
	def __init__(self, returnType, parameterTypes):
		self.returnType = returnType
		self.parameterTypes = parameterTypes

	def __eq__(self, other):
		if (other == None):
			return False
		parametersLength = len(self.parameterTypes)
		ans = self.returnType == other.returnType and parametersLength == len(other.parameterTypes)
		if (not ans):
			return False
		for i in range(parametersLength):
			if (self.parameterTypes[i] != other.parameterTypes[i]):
				return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return "function "+str(self.returnType)+" ["+", ".join(map(str,self.parameterTypes))+"]"

def solveType(expr):
	if (isinstance(expr, Symbol)):
		expr = expr.value()
		if (expr == "str"):
			return str
		elif (expr =="bool"):
			return bool
		elif (expr =="int"):
			return int
		elif (expr =="float"):
			return float
		else:
			raise ValueError(expr + 'is not a valid type.')
	try:
		if expr[0].value() == "function":
			returnType = solveType(expr[1])
			parameterTypes = []
			for parameter in expr[2].value():
				parameterTypes.append(solveType(parameter))
			return FunctionType(returnType, parameterTypes)
		else:
			raise ValueError(str(expr) + 'is not a valid type.')	
	except:
		raise ValueError(str(expr) + 'is not a valid type.')

class Environment:
	def __init__(self):
		self.dictionary = {}

	def put(self, key, value):
		self.dictionary[key] = value

	def get(self, key):
		value = self.dictionary[key]
		if (value == None):
			raise ValueError(key + ' was not declared in this scope.')
		return value

	def clone(self):
		newEnv = Environment()
		newEnv.dictionary = self.dictionary.copy()
		return newEnv
