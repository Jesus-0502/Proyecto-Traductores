reserved = {
    'if': 'TkIf',
    'while': 'TkWhile',
    'end': 'TkEnd',
    'int': 'TkInt',
    'function': 'TkFunction',
    'print': 'TkPrint',
    'true': 'TkTrue',
    'false': 'TkFalse',
    'or': 'TkOr',
    'and': 'TkAnd'
}

tokens = list(reserved.values()) + [
    'TkId', 'TkNum', 'TkString',
    'TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 'TkSemicolon', 'TkArrow', 'TkGuard',
    'TkPlus', 'TkMinus', 'TkMult', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 'TkNEqual',
    'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkApp',
    'ERROR'
]