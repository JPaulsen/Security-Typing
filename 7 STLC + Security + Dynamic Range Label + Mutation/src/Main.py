from Parser import *
from TypeChecker import *
from Interpreter import *

codeSource = open("input.txt", "r")

print "+--------------------+"
for code in codeSource:
    if code[-1] == "\n":
        code = code[:-1]
    print "Code:", code
    program = loads(code, true='True', false='False')
    print "Program:", program
    ast = parse(program)
    print "AST before typeCheck:", ast
    typeCheckerResult = typeCheck(ast)
    type = typeCheckerResult.type
    print "Type:", type
    ast = typeCheckerResult.astNode
    print "AST after typeCheck:", ast
    print "Result:", interp(ast)
    print "+--------------------+"
