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
        "code": "(set x (int 1) (get x))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(function int [int int] [x y] (+ (get x) (get y)))",
        "expectedValue": "function <type 'int'> [<type 'int'>, <type 'int'>]"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function int [int int] [x y] (+ (get x) (get y))) [(int 1) (int 2)])",
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
        "code": "(function int [int int] [x y] (or (get x) (get y)))",
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
        "code": "(set x (int 3) (get x))",
        "expectedValue": "<type 'int'>"
    },
    {
        "command": "typeCheck",
        "code": "(function int [] [] (int 3))",
        "expectedValue": "function <type 'int'> []"
    },
    {
        "command": "typeCheck",
        "code": "(set f (function int [int int] [x y] (+ (get x) (get y))) (apply (get f) [(int 1) (int 2)]))",
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
        "code": "(set x (int 1) (get x))",
        "expectedValue": "1",
    },
    {
        "command": "interp",
        "code": "(function int [int int] [x y] (+ (get x) (get y)))",
        "expectedValue": "function <type 'int'> [<type 'int'>, <type 'int'>] [Symbol('x'), Symbol('y')] (+ (get Symbol('x')) (get Symbol('y')))",
    },
    {
        "command": "interp",
        "code": "(apply (function int [int int] [x y] (+ (get x) (get y))) [(int 1) (int 2)])",
        "expectedValue": "3",
    },
    {
        "command": "interp",
        "code": "(/ (int 1) (int 0))",
        "expectedValue": "Runtime Error",
    },
    {
        "command": "interp",
        "code": "(set myApply (function int [(function int [int int])] [f] (apply (get f) [(int 0) (int 1)])) (apply (get myApply) [(function int [int int] [x y] (+ (get x) (get y)))]))",
        "expectedValue": "1",
    },
]
