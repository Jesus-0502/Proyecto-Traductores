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

t_TkOBlock = r'\{'
t_TkCBlock = r'\}'
t_TkComma = r','
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkAsig = r':='
t_TkSemicolon = r';'
t_TkArrow = r'-->'
t_TkGuard = r'\[\]'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkMult = r'\*'
t_TkNot = r'!'
t_TkLess = r'<'
t_TkLeq = r'<='
t_TkGeq = r'>='
t_TkGreater = r'>'
t_TkEqual = r'=='
t_TkNEqual = r'<>'
t_TkOBracket = r'\['
t_TkCBracket = r'\]'
t_TkTwoPoints = r':'
t_TkApp = r'\.'
t_TkSoForth = r'\.\.'

t_ignore = ' \t'

def t_comment(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_TkString(t):
    r'"([^\n\\"]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TkId(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'TkId')
    return t

def t_ERROR(t):
    r'.'
    return t

def t_error(t):
    t.type = 'ERROR'
    return t
