from AST import *

class Interpreter:
	def visitBoolLiteral(self, boolLiteral, env):
		return boolLiteral.value

	def visitIntLiteral(self, intLiteral, env):
		return intLiteral.value

	def visitFloatLiteral(self, floatLiteral, env):
		return floatLiteral.value

	def visitStringLiteral(self, stringLiteral, env):
		return stringLiteral.value

	def visitUnaryExpression(self, unaryExpression, env):
		if (unaryExpression.command == "not"):
			return not unaryExpression.expression.accept(self, env)
		raise ValueError("UnaryExpression with command "+unaryExpression.command+" not yet implementd.")

	def visitBinaryExpression(self, binaryExpression, env):
		if (binaryExpression.command == "and"):
			return binaryExpression.firstExpression.accept(self, env) and binaryExpression.secondExpression.accept(self, env)
		elif (binaryExpression.command == "or"):
			return binaryExpression.firstExpression.accept(self, env) or binaryExpression.secondExpression.accept(self, env)
		elif (binaryExpression.command == "+"):
			return binaryExpression.firstExpression.accept(self, env) + binaryExpression.secondExpression.accept(self, env)
		elif (binaryExpression.command == "-"):
			return binaryExpression.firstExpression.accept(self, env) - binaryExpression.secondExpression.accept(self, env)
		elif (binaryExpression.command == "*"):
			return binaryExpression.firstExpression.accept(self, env) * binaryExpression.secondExpression.accept(self, env)
		elif (binaryExpression.command == "/"):
			return binaryExpression.firstExpression.accept(self, env) / binaryExpression.secondExpression.accept(self, env)
		raise ValueError("BinaryExpression with command "+binaryExpression.command+" not yet implementd.") 	

	def visitIfExpression(self, ifExpression, env):
		if (ifExpression.cond.accept(self, env)):
			return thenExpression.accept(self, env)
		else:
			return elseExpression.accept(self, env)	

	def visitSetExpression(self, setExpression, env):
		newEnv = env.clone()
		newEnv.put(setExpression.symbol.value(), setExpression.valueExpression.accept(self, env))
		return setExpression.thenExpression.accept(self, newEnv)

	def visitGetExpression(self, getExpression, env):
		return env.get(getExpression.symbol.value())

	def visitFunctionExpression(self, functionExpression, env):
		return functionExpression

	def visitApplyExpression(self, applyExpression, env):
		functionExpression = applyExpression.functionExpression.accept(self, env)
		arguments = []
		for argument in applyExpression.argumentExpressions:
			arguments.append(argument.accept(self, env))
		newEnv = Environment()
		argumentsLength = len(arguments)
		for i in range(argumentsLength):
			newEnv.put(functionExpression.parameterSymbols[i].value(), arguments[i])
		return functionExpression.bodyExpression.accept(self, newEnv)

def interp(ast):
	return ast.accept(Interpreter(), Environment())
