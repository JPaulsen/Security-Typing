import sys

sys.path.insert(0, '../src/')

from Parser import *
from TypeChecker import *
from Interpreter import *


def safeTypeCheck(code):
    try:
        program = loads(code, true='True', false='False')
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
        program = loads(code, true='True', false='False')
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
