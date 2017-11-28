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
        "command": "interp",
        "code": "(function l (function l (int l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "((function (function (<type 'int'>, l) [(<type 'int'>, l)], l) [], l) [] (function (<type 'int'>, l) [(<type 'int'>, l)], l) [Symbol('x')] (+ (get Symbol('x')) (int 1)), l)"
    },
    {
        "command": "typeCheck",
        "code": "(function l (function l (bool l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function l (bool ?) [((function ? (bool ?) [(bool ?)]) f)] (apply (f) [(bool h True)])) [(function l (bool l) [((bool l) x)] (bool l True))])",
        "expectedValue": "(<type 'bool'>, (b, t))",
    },
    {
        "command": "interp",
        "code": "(apply (function l (bool ?) [((function ? (bool ?) [(bool ?)]) f)] (apply (f) [(bool h True)])) [(function l (bool l) [((bool l) x)] (bool l True))])",
        "expectedValue": "Runtime Error",
    },
    {
        "command": "interp",
        "code": "(function l (function l (int l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "((function (function (<type 'int'>, l) [(<type 'int'>, l)], l) [], l) [] (function (<type 'int'>, l) [(<type 'int'>, l)], l) [Symbol('x')] (+ (get Symbol('x')) (int 1)), l)",
    },
    {
        "command": "typeCheck",
        "code": "(function l (function l (bool l) [(int l)]) [] (function l (int l) [((int l) x)] (+ (x) (int l 1))))",
        "expectedValue": "Type Error",
    },
    {
        "command": "typeCheck",
        "code": "(apply (function l (bool l) [((function l (bool l) []) f)] (apply (f) [])) [(function l (bool ?) [] (bool h True))])",
        "expectedValue": "(<type 'bool'>, l)",
    },
    {
        "command": "interp",
        "code": "(apply (function l (bool l) [((function l (bool l) []) f)] (apply (f) [])) [(function l (bool ?) [] (bool h True))])",
        "expectedValue": "Runtime Error",
    },
    {
        "command": "typeCheck",
        "code": "(apply (function l (int ?) [((function l (int l) []) f)] (apply (f) [])) [(function l (int ?) [] (int h 1))])",
        "expectedValue": "(<type 'int'>, (b, t))",
    },
    {
        "command": "interp",
        "code": "(apply (function l (int ?) [((function l (int l) []) f)] (apply (f) [])) [(function l (int ?) [] (int h 1))])",
        "expectedValue": "Runtime Error",
    },
    {
        "command": "typeCheck",
        "code": "(let x (ref (int l)) (if (bool h True) (assign (x) (int l 0) (x)) (assign (x) (int l 1) (x))))",
        "expectedValue": "Type Error"
    },
    {
        "command": "typeCheck",
        "code": "(function l (int l) [((int h) x) ((int ?) y)] (+ (x) (y)))",
        "expectedValue": "(function (<type 'int'>, l) [(<type 'int'>, h), (<type 'int'>, (b, t))], l)"
    },
    {
        "command": "interp",
        "code": "(function l (int l) [((int h) x) ((int ?) y)] (+ (x) (y)))",
        "expectedValue": "((function (<type 'int'>, l) [(<type 'int'>, h), (<type 'int'>, (b, t))], l) [Symbol('x'), Symbol('y')] (check [(<type 'int'>, l)] (+ (get Symbol('x')) (get Symbol('y')))), l)"
    },
    {
        "command": "typeCheck",
        "code": "(apply (function l (int l) [((int h) x) ((int ?) y)] (let a (ref (int l)) (assign (a) (+ (x) (y)) (deref (a))))) [(int h 1) (int ? 2)])",
        "expectedValue": "(<type 'int'>, l)"
    },
    {
        "command": "interp",
        "code": "(apply (function l (int l) [((int h) x) ((int ?) y)] (let a (ref (int l)) (assign (a) (+ (x) (y)) (deref (a))))) [(int h 1) (int ? 2)])",
        "expectedValue": "Runtime Error"
    },
    {
        "command": "interp",
        "code": "(if (bool h True) (int h 1) (int h 0))",
        "expectedValue": "(1, h)"
    },
    {
        "command": "interp",
        "code": "(if (bool h False) (int h 1) (int h 0))",
        "expectedValue": "(0, h)"
    },
    {
        "command": "interp",
        "code": "(apply (function h (int h) [((function ? (int h) []) f)] (apply (f) [])) [(function l (int h) [] (int h 1))])",
        "expectedValue": "Runtime Error"
    },
    {
        "command": "interp",
        "code": "(let x (ref (int ?)) (assign (x) (int h 0) (let y (ref (int l)) (assign (y) (deref (x)) (y)))))",
        "expectedValue": "Runtime Error"
    },

]
