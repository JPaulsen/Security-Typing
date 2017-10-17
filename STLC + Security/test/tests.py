tests = [
    {
        "command": "typeCheck",
        "code": "(bool h True)",
        "expectedValue": "(<type 'bool'>, h)"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function h (int h) [((int l) x)] (x)) [(int l 3)])",
        "expectedValue": "(<type 'int'>, h)"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function h (int l) [((int h) x)] (x)) [(int h 3)])",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function h (int l) [((int l) x)] (x)) [(int h 3)])",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function l (bool l) [((function l (bool l) [(bool l)]) f)] (apply (f) [(bool l True)])) [(function l (bool l) [((bool l) x)] (bool l True))])",
        "expectedValue": "(<type 'bool'>, l)",
    },
    {
        "command": "interp",
        "code": "(function l (function l (int l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "(function (function (<type 'int'>, l) [(<type 'int'>, l)], l) [], l) [] (function (<type 'int'>, l) [(<type 'int'>, l)], l) [Symbol('x')] (+ (get Symbol('x')) (int 1))"
    },
    {
        "command": "typeCheck",
        "code": "(function l (function l (bool l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "Type Error"
    },
]
