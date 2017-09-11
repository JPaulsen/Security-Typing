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
        "code": "(let x (ref (int l)) (if (bool h True) (assign (x) (int l 0) (x)) (assign (x) (int l 1) (x))))",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(let f (function l (int l) [] (int l 0)) (if (bool h True) (apply (f) []) (apply (f) [])))",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(function l (int l) [((ref (int b)) x)] (assign (x) (int b 0) (int l 1)))",
        "expectedValue": "Type Error"
    },
]