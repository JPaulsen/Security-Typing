from Compiler import *
from Interpreter import *

while(True):
	try:
		code = raw_input()
	except:
		break
	program = loads(code, true = 'True', false = 'False')
	ast = compile(program)
	print ast
	print interp(ast)
