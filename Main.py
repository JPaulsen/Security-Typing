from Parser import *
from TypeChecker import *
from Interpreter import *

print "+--------------------+"
while(True):
	try:
		code = raw_input()
	except:
		break
	program = loads(code, true = 'True', false = 'False')
	ast = parse(program)
	print ast
	print typeCheck(ast)
	print interp(ast)
	print "+--------------------+"
