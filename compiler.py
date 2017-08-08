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
	value1 = _compile(expr[1], env)
	value2 = _compile(expr[2], env)
	_checkExpectedTypes(value1.expressionType, [bool])
	_checkExpectedTypes(value2.expressionType, [bool])
	return BinaryExpression(bool, command, value1, value2)

def _checkNumericBinaryExpression(command, expr, env):
	_checkLengthExpected(command, expr, 3)
	value1 = _compile(expr[1], env)
	value2 = _compile(expr[2], env)
	_checkExpectedTypes(value1.expressionType, [int, float])
	_checkExpectedTypes(value2.expressionType, [int, float])
	ans = int
	if (value1.expressionType == float or value2.expressionType == float):
		ans = float
	return BinaryExpression(ans, command, value1, value2)

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
		value = _compile(expr[1], env)
		_checkExpectedTypes(value.expressionType, [bool])
		return UnaryExpression(bool, "not", value)
	elif (command == "and" or command == "or"):
		return _checkBooleanBinaryExpression(command, expr, env)
	elif (command == "+" or command == "-" or command == "*" or command == "/"):
		return _checkNumericBinaryExpression(command, expr, env)
	elif (command == "if"):
		_checkLengthExpected("if", expr, 4)
		cond = _compile(expr[1], env)
		_checkExpectedTypes(cond, [bool])
		thenExpression = _compile(expr[3], env)
		elseExpression = _compile(expr[4], env)
		_checkExpectedTypes(elseExpression.expressionType, [thenExpression.expressionType])
		return IfExpression(cond, thenExpression, elseExpression)
	elif (command == "set"):
		_checkLengthExpected("set", expr, 4)
		symbol = expr[1]
		if (not isinstance(symbol, Symbol)):
			raise ValueError('set first argument must be a symbol.')
		value = _compile(expr[2], env)
		newEnv = env.clone()
		newEnv.put(symbol.value(), value.expressionType)
		body = _compile(expr[3], newEnv)
		return SetExpression(symbol, value, body)
	elif (command == "get"):
		_checkLengthExpected("get", expr, 2)
		var = expr[1]
		if (not isinstance(var, Symbol)):
			raise ValueError('get argument must be a symbol.')
		return GetExpression(env.get(var.value()), var)
	elif (command == "function"):
		functionType = solveType(expr)
		params = expr[3].value()
		body = expr[4]
		paramsLength = len(params)
		if (paramsLength != len(functionType.paramTypes)):
			raise ValueError('Function length of types and parameters do not match.')
		newEnv = Environment()
		for i in range(paramsLength):
			symbol = params[i]
			if (not isinstance(symbol, Symbol)):
				raise ValueError('Each function parameter must be a symbol.')
			newEnv.put(symbol.value(), functionType.paramTypes[i])
		returnType = _compile(body, newEnv)
		if (functionType.returnType != returnType.expressionType):
			raise ValueError('Body return type does not match Function return type.')
		return FunctionExpression(functionType, params, returnType)
	elif (command == "apply"):
		functionType = _compile(expr[1], env)
		arguments = []
		for arg in expr[2].value():
			arguments.append(_compile(arg, env))
		return ApplyExpression(functionType, arguments)
	else:
		raise ValueError('command ' + command + ' not defined.')
		