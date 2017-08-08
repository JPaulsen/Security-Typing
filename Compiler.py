from AST import *

def _checkLengthExpected(name, expr, n):
	if (len(expr) != n):
		lastPart = ' elements.'
		if (n == 1):
			lastPart = ' element.'
		raise ValueError(name + ' expressions must have ' + n + lastPart) 	

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

def _checkBooleanBinaryExpression(command, expr, env):
	_checkLengthExpected(command, expr, 3)
	firstExpression = _compile(expr[1], env)
	secondExpression = _compile(expr[2], env)
	_checkExpectedTypes(firstExpression.expressionType, [bool])
	_checkExpectedTypes(secondExpression.expressionType, [bool])
	return BinaryExpression(bool, command, firstExpression, secondExpression)

def _checkNumericBinaryExpression(command, expr, env):
	_checkLengthExpected(command, expr, 3)
	firstExpression = _compile(expr[1], env)
	secondExpression = _compile(expr[2], env)
	_checkExpectedTypes(firstExpression.expressionType, [int, float])
	_checkExpectedTypes(secondExpression.expressionType, [int, float])
	expressionType = int
	if (firstExpression.expressionType == float or secondExpression.expressionType == float):
		expressionType = float
	return BinaryExpression(expressionType, command, firstExpression, secondExpression)

def compile(expr):
	return _compile(expr, Environment())

def _compile(expr, env):
	if (len(expr) == 0):
		raise ValueError('expressions can not be empty.')
	command = expr[0]
	if (not isinstance(command, Symbol)):
		raise ValueError('first keyword of a expression must be a symbol.')
	command = command.value()
	if (command == 'bool'):
		_checkLengthExpected("Boolean literal", expr, 2)
		value = expr[1]
		_checkExpectedTypesOfValue(value, [bool])
		return BoolLiteral(value)
	elif (command == 'int'):
		_checkLengthExpected("Integer literal", expr, 2)
		value = expr[1]
		_checkExpectedTypesOfValue(value, [int])
		return IntLiteral(value)
	elif (command == 'float'):
		_checkLengthExpected("Float literal", expr, 2)
		value = expr[1]
		_checkExpectedTypesOfValue(value, [int, float])
		return FloatLiteral(value)
	elif (command == 'str'):
		_checkLengthExpected("String literal", expr, 2)
		value = expr[1]
		_checkExpectedTypesOfValue(value, [str])
		return StringLiteral(value)
	elif (command == "not"):
		_checkLengthExpected("not", expr, 2)
		expression = _compile(expr[1], env)
		_checkExpectedTypes(expression.expressionType, [bool])
		return UnaryExpression(bool, "not", expression)
	elif (command == "and" or command == "or"):
		return _checkBooleanBinaryExpression(command, expr, env)
	elif (command == "+" or command == "-" or command == "*" or command == "/"):
		return _checkNumericBinaryExpression(command, expr, env)
	elif (command == "if"):
		_checkLengthExpected("if", expr, 4)
		conditionExpression = _compile(expr[1], env)
		_checkExpectedTypes(conditionExpression, [bool])
		thenExpression = _compile(expr[3], env)
		elseExpression = _compile(expr[4], env)
		_checkExpectedTypes(elseExpression.expressionType, [thenExpression.expressionType])
		return IfExpression(conditionExpression, thenExpression, elseExpression)
	elif (command == "set"):
		_checkLengthExpected("set", expr, 4)
		symbol = expr[1]
		if (not isinstance(symbol, Symbol)):
			raise ValueError('set first argument must be a symbol.')
		valueExpression = _compile(expr[2], env)
		newEnv = env.clone()
		newEnv.put(symbol.value(), valueExpression.expressionType)
		thenExpression = _compile(expr[3], newEnv)
		return SetExpression(symbol, valueExpression, thenExpression)
	elif (command == "get"):
		_checkLengthExpected("get", expr, 2)
		symbol = expr[1]
		if (not isinstance(symbol, Symbol)):
			raise ValueError('get argument must be a symbol.')
		return GetExpression(env.get(symbol.value()), symbol)
	elif (command == "function"):
		_checkLengthExpected("function", expr, 5)
		functionType = solveType(expr)
		parameterSymbols = expr[3].value()
		parametersLength = len(parameterSymbols)
		if (parametersLength != len(functionType.parameterTypes)):
			raise ValueError('Function length of types and parameters do not match.')
		newEnv = Environment()
		for i in range(parametersLength):
			symbol = parameterSymbols[i]
			if (not isinstance(symbol, Symbol)):
				raise ValueError('Each function parameter must be a symbol.')
			newEnv.put(symbol.value(), functionType.parameterTypes[i])
		bodyExpression = _compile(expr[4], newEnv)
		if (functionType.returnType != bodyExpression.expressionType):
			raise ValueError('Body return type does not match Function return type.')
		return FunctionExpression(functionType, parameterSymbols, bodyExpression)
	elif (command == "apply"):
		_checkLengthExpected("apply", expr, 3)
		functionExpression = _compile(expr[1], env)
		argumentExpressions = []
		for argumentExpression in expr[2].value():
			argumentExpressions.append(_compile(argumentExpression, env))
		parametersLength = len(functionExpression.expressionType.parameterTypes)
		if (parametersLength != len(argumentExpressions)):
			raise ValueError('Function length of parameters and arguments in apply do not match.')
		return ApplyExpression(functionExpression, argumentExpressions)
	else:
		raise ValueError('command ' + command + ' not defined.')
		