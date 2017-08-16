from AST import *

def _checkExpectedTypesOfValue(value, types):
	for type in types:
		if (isinstance(value, type)):
			return;
	raise ValueError(' or '.join(map(str, types)) + ' was expected.')

def _checkExpectedTypes(type, types):
	for t in types:
		if type == t:
			return;
	raise ValueError(' or '.join(map(str, types)) + ' was expected.')	

def typeCheck(ast):
	return ast.accept(TypeChecker(), Environment())

class TypeChecker:
	def visitBoolLiteral(self, boolLiteral, env):
		_checkExpectedTypesOfValue(boolLiteral.value, [bool])
		return bool

	def visitIntLiteral(self, intLiteral, env):
		_checkExpectedTypesOfValue(intLiteral.value, [int])
		return int

	def visitFloatLiteral(self, floatLiteral, env):
		_checkExpectedTypesOfValue(floatLiteral.value, [int, float])
		return float

	def visitStringLiteral(self, stringLiteral, env):
		_checkExpectedTypesOfValue(stringLiteral.value, [str])
		return str

	def visitUnaryExpression(self, unaryExpression, env):
		if (unaryExpression.command == "not"):
			_checkExpectedTypes(unaryExpression.expression.accept(self, env), [bool])
			return bool
		raise ValueError("UnaryExpression with command "+unaryExpression.command+" not yet implementd at typeChecker level.")

	def visitBinaryExpression(self, binaryExpression, env):
		if (binaryExpression.command == "and" or binaryExpression.command == "or"):
			_checkExpectedTypes(binaryExpression.firstExpression.accept(self, env), [bool])
			_checkExpectedTypes(binaryExpression.secondExpression.accept(self, env), [bool])
			return bool
		elif (binaryExpression.command == "+" or binaryExpression.command == "-" or binaryExpression.command == "*" or binaryExpression.command == "/"):
			firstExpressionType = binaryExpression.firstExpression.accept(self, env)
			secondExpressionType = binaryExpression.secondExpression.accept(self, env)
			_checkExpectedTypes(firstExpressionType, [int, float])
			_checkExpectedTypes(secondExpressionType, [int, float])
			return float if firstExpressionType == float or secondExpressionType == float else int
		raise ValueError("BinaryExpression with command "+binaryExpression.command+" not yet implementd.") 	

	def visitIfExpression(self, ifExpression, env):
		_checkExpectedTypes(ifExpression.conditionExpression.accept(self, env), [bool])
		thenExpressionType = ifExpression.thenExpression.accept(self, env)
		elseExpressionType = ifExpression.elseExpression.accept(self, env)
		_checkExpectedTypes(elseExpressionType, [thenExpressionType])
		return thenExpressionType

	def visitSetExpression(self, setExpression, env):
		newEnv = env.clone()
		newEnv.put(setExpression.symbol.value(), setExpression.valueExpression.accept(self, env))
		return setExpression.thenExpression.accept(self, newEnv)

	def visitGetExpression(self, getExpression, env):
		return env.get(getExpression.symbol.value())

	def visitFunctionExpression(self, functionExpression, env):
		functionType = functionExpression.functionType
		parametersLength = len(functionType.parameterTypes)
		newEnv = Environment()
		for i in range(parametersLength):
			symbol = functionExpression.parameterSymbols[i]
			if (not isinstance(symbol, Symbol)):
				raise ValueError('Each function parameter must be a symbol.')
			newEnv.put(functionExpression.parameterSymbols[i].value(), functionType.parameterTypes[i])
		bodyExpressionType = functionExpression.bodyExpression.accept(self, newEnv)
		if (functionType.returnType != bodyExpressionType):
			raise ValueError('Body return type does not match Function return type.')
		return functionType

	def visitApplyExpression(self, applyExpression, env):
		functionType = applyExpression.functionExpression.accept(self, env)
		argumentTypes = []
		for argument in applyExpression.argumentExpressions:
			argumentTypes.append(argument.accept(self, env))
		argumentsLength = len(argumentTypes)
		if (len(functionType.parameterTypes) != argumentsLength):
			raise ValueError('Function length of parameters and arguments in apply do not match.')
		for i in range(argumentsLength):
			parameterType = functionType.parameterTypes[i]
			argumentType = argumentTypes[i]
			_checkExpectedTypes(argumentType, [parameterType])
		return functionType.returnType
