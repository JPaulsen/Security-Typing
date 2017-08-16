from sexpdata import *

class BoolLiteral:
	def __init__(self, value):
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitBoolLiteral(self, env)

	def __str__(self):
		return "(bool " + str(self.value) + ")"

class IntLiteral:
	def __init__(self, value):
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitIntLiteral(self, env)

	def __str__(self):
		return "(int " + str(self.value) + ")"

class FloatLiteral:
	def __init__(self, value):
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitFloatLiteral(self, env)

	def __str__(self):
		return "(float " + str(self.value) + ")"

class StringLiteral:
	def __init__(self, value):
		self.value = value

	def accept(self, visitor, env):
		return visitor.visitStringLiteral(self, env)

	def __str__(self):
		return "(str " + str(self.value) + ")"

class UnaryExpression:
	def __init__(self, command, expression):
		self.command = command
		self.expression = expression

	def accept(self, visitor, env):
		return visitor.visitUnaryExpression(self, env)

	def __str__(self):
		return "(" + self.command + " " + str(self.expression) + ")"

class BinaryExpression:
	def __init__(self, command, firstExpression, secondExpression):
		self.command = command
		self.firstExpression = firstExpression
		self.secondExpression = secondExpression

	def accept(self, visitor, env):
		return visitor.visitBinaryExpression(self, env)

	def __str__(self):
		return "(" + self.command + " " + str(self.firstExpression) + " " + str(self.secondExpression) + ")"

class IfExpression:
	def __init__(self, conditionExpression, thenExpression, elseExpression):
		self.conditionExpression = conditionExpression
		self.thenExpression = thenExpression
		self.elseExpression = elseExpression

	def accept(self, visitor, env):
		return visitor.visitIfExpression(self, env)

	def __str__(self):
		return "(if " + str(self.conditionExpression) + " " + str(self.thenExpression) + " " + str(self.elseExpression) + ")"

class SetExpression:
	def __init__(self, symbol, valueExpression, thenExpression):
		self.symbol = symbol
		self.valueExpression = valueExpression
		self.thenExpression = thenExpression

	def accept(self, visitor, env):
		return visitor.visitSetExpression(self, env)

	def __str__(self):
		return "(set " + str(self.symbol) + " " + str(self.valueExpression) + " " + str(self.thenExpression) + ")"

class GetExpression:
	def __init__(self, symbol):
		self.symbol = symbol

	def accept(self, visitor, env):
		return visitor.visitGetExpression(self, env)

	def __str__(self):
		return "(get " + str(self.symbol) + ")"

class FunctionExpression:
	def __init__(self, functionType, parameterSymbols, bodyExpression):
		self.functionType = functionType
		self.parameterSymbols = parameterSymbols
		self.bodyExpression = bodyExpression

	def accept(self, visitor, env):
		return visitor.visitFunctionExpression(self, env)

	def __str__(self):
		return str(self.functionType) + " [" + ", ".join(map(str,self.parameterSymbols))+"] " + str(self.bodyExpression)

class ApplyExpression:
	def __init__(self, functionExpression, argumentExpressions):
		self.functionExpression = functionExpression
		self.argumentExpressions = argumentExpressions

	def accept(self, visitor, env):
		return visitor.visitApplyExpression(self, env)

	def __str__(self):
		return "(apply " + str(self.functionExpression) + " " + ", ".join(map(str,self.argumentExpressions)) + ")"

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
