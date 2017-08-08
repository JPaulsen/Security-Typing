import sys
sys.path.insert(0, '..')
import shlex

from Compiler import *
from Interpreter import *

def safeCompile(code):
	try:
		program = loads(code, true = 'True', false = 'False')
	except:
		return "Format Error"
	try:
		return compile(program)
	except:
		return "Runtime Error"

def safeInterp(ast):
	try:
		return interp(ast)
	except:
		return "Runtime Error"

def printPassed(test):
	print "Test "+ str(test) +": PASSED"

def printFailed(test, expected, result):
	print "Test "+ str(test) +": FAILED, expected: "+ expected + ", found: " + result

def printBadCommand(test, command):
	print "Test "+ str(test) +": WRONG COMMAND: "+command

test = 0
failed = 0
while(True):
	try:
		code = shlex.split(raw_input())
	except:
		break
	command = code[0]
	expected = code[1]
	code = code[2]
	test += 1
	if (command == "compile"):
		result = str(safeCompile(code))
	elif (command == "interp"):
		result = str(safeInterp(compile(loads(code, true = 'True', false = 'False'))))
	else:
		printBadCommand(test, command)
		failed += 1
		continue
	if (result == expected):
		printPassed(test)
	else:
		printFailed(test, expected, result)
		failed += 1

print "Total amount of tests: "+str(test)+", tests passed: "+str(test-failed)+", tests failed: "+str(failed)+"."
if (failed > 0):
	print "Some tests failed."
else:
	print "All test passed!"
