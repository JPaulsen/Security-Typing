import sys
sys.path.insert(0, '..')
import shlex

from Parser import *
from TypeChecker import *
from Interpreter import *

def safeTypeCheck(code):
	try:
		program = loads(code, true = 'True', false = 'False')
	except:
		return "Syntax Error"
	try:
		ast = parse(program)
	except:
		return "Parsing Error"
	try:
		return typeCheck(ast)
	except:
		return "Type Error"

def safeInterp(code):
	try:
		program = loads(code, true = 'True', false = 'False')
	except:
		return "Syntax Error"
	try:
		ast = parse(program)
	except:
		return "Parsing Error"
	try:
		typeCheck(ast)
	except:
		return "Type Error"
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
	if (command == "typeCheck"):
		result = str(safeTypeCheck(code))
	elif (command == "interp"):
		result = str(safeInterp(code))
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
