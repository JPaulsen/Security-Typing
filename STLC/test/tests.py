tests = [
    {
        "command": "typeCheck",
        "code": "(bool True)",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(int 0)",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(float 0)",
        "expectedValue": "<type 'float'>"
    },
    {
        "command": "typeCheck",
        "code": "(float 0.0)",
        "expectedValue": "<type 'float'>"
    },
    {
        "command": "typeCheck",
        "code": "(str \"0.0\")",
        "expectedValue": "<type 'str'>"
    },
    {
        "command": "typeCheck",
        "code": "(not (bool True))",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(and (bool True) (bool False))",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(or (bool True) (bool False))",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(+ (int 10) (int 5))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(- (int 10) (int 5))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(* (int 10) (int 5))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(/ (int 10) (int 5))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(if (bool True) (int 1) (int 0))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(let x (int 1) (x))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(function (int) [((int) x) ((int) y)] (+ (x) (y)))",
        "expectedValue": "function <type 'int'> [<type 'int'>, <type 'int'>]"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function (int) [((int) x) ((int) y)] (+ (x) (y))) [(int 1) (int 2)])",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(bool 0)",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(int 0.0)",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(float \"0.0\")",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(str True)",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(function (int) [((int) x) ((int) y)] (or (x) (y)))",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(* (+ (int 3) (int 5)) (- (int 4) (float 3.0)))",
        "expectedValue": "<type 'float'>"
    },
    {
        "command": "typeCheck",
        "code": "(and (bool True) (bool False))",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(or (bool True) (bool False))",
        "expectedValue": "<type 'bool'>"
    },
    {
        "command": "typeCheck",
        "code": "(let x (int 3) (x))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(function (int) [] (int 3))",
        "expectedValue": "function <type 'int'> []"
    },
    {
        "command": "typeCheck",
        "code": "(let f (function (int) [((int) x) ((int) y)] (+ (x) (y))) (apply (f) [(int 1) (int 2)]))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "interp",
        "code": "(bool True)",
        "expectedValue": "True",
    },
    {
        "command": "interp",
        "code": "(int 0)",
        "expectedValue": "0",
    },
    {
        "command": "interp",
        "code": "(float 0)",
        "expectedValue": "0.0",
    },
    {
        "command": "interp",
        "code": "(float 0.0)",
        "expectedValue": "0.0",
    },
    {
        "command": "interp",
        "code": "(str \"0.0\")",
        "expectedValue": "0.0",
    },
    {
        "command": "interp",
        "code": "(not (bool True))",
        "expectedValue": "False",
    },
    {
        "command": "interp",
        "code": "(and (bool True) (bool False))",
        "expectedValue": "False",
    },
    {
        "command": "interp",
        "code": "(or (bool True) (bool False))",
        "expectedValue": "True",
    },
    {
        "command": "interp",
        "code": "(+ (int 10) (int 5))",
        "expectedValue": "15",
    },
    {
        "command": "interp",
        "code": "(- (int 10) (int 5))",
        "expectedValue": "5",
    },
    {
        "command": "interp",
        "code": "(* (int 10) (int 5))",
        "expectedValue": "50",
    },
    {
        "command": "interp",
        "code": "(/ (int 10) (int 5))",
        "expectedValue": "2",
    },
    {
        "command": "interp",
        "code": "(if (bool True) (int 1) (int 0))",
        "expectedValue": "1",
    },
    {
        "command": "interp",
        "code": "(let x (int 1) (x))",
        "expectedValue": "1",
    },
    {
        "command": "interp",
        "code": "(function (int) [((int) x) ((int) y)] (+ (x) (y)))",
        "expectedValue": "function <type 'int'> [<type 'int'>, <type 'int'>] [Symbol('x'), Symbol('y')] (+ (Symbol('x')) (Symbol('y')))",
    },
    {
        "command": "interp",
        "code": "(apply (function (int) [((int) x) ((int) y)] (+ (x) (y))) [(int 1) (int 2)])",
        "expectedValue": "3",
    },
    {
        "command": "interp",
        "code": "(/ (int 1) (int 0))",
        "expectedValue": "Runtime Error",
    },
    {
        "command": "interp",
        "code": "(let myApply (function (int) [((function (int) [(int) (int)]) f)] (apply (f) [(int 0) (int 1)])) (apply (myApply) [(function (int) [((int) x) ((int) y)] (+ (x) (y)))]))",
        "expectedValue": "1",
    },
    {
        "command": "interp",
        "code": "(let x (int 0) (let y (apply (function (int) [((int) x)] (x)) [(int 3)]) (x)))",
        "expectedValue": "0",
    },
]
