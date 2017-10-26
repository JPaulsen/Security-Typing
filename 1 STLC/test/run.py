import unittest

from tests import *
from util import *


class StclTests(unittest.TestCase):
    def test(self):
        for test in tests:
            if (test['command'] == "typeCheck"):
                result = str(safeTypeCheck(test['code']))
            elif (test['command'] == "interp"):
                result = str(safeInterp(test['code']))
            try:
                self.assertEqual(result, test['expectedValue'])
            except:
                testCode = "####################\n"
                testCode += "Failed test:\n"
                testCode += "command = " + test["command"] + "\n"
                testCode += "code = " + test["code"] + "\n"
                testCode += "expectedValue = " + test["expectedValue"] + "\n"
                testCode += "result = " + result + "\n"
                testCode += "####################\n\n"
                print testCode
                raise


suite = unittest.TestLoader().loadTestsFromTestCase(StclTests)
unittest.TextTestRunner(verbosity=0).run(suite)
