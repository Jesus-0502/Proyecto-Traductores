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
    'and': 'TkAnd',
    'fi': 'TkFi',
    'else': 'TkElse',
    'bool': 'TkBool',
    'skip': 'TkSkip'
}

tokens = list(reserved.values()) + [
    'TkId', 'TkNum', 'TkString',
    'TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 'TkSemicolon', 'TkArrow', 'TkGuard',
    'TkPlus', 'TkMinus', 'TkMult', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 'TkNEqual',
    'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkApp',
    'ERROR'
]

def t_TkOBlock(t):
    r'\{'
    return t

def t_TkCBlock(t):
    r'\}'
    return t

def t_TkComma(t):
    r','
    return t

def t_TkOpenPar(t):
    r'\('
    return t

def t_TkClosePar(t):
    r'\)'
    return t

def t_TkAsig(t):
    r':='
    return t

def t_TkSemicolon(t):
    r';'
    return t

def t_TkArrow(t):
    r'-->'
    return t

def t_TkGuard(t):
    r'\[\]'
    return t

def t_TkPlus(t):
    r'\+'
    return t

def t_TkMinus(t):
    r'-'
    return t

def t_TkMult(t):
    r'\*'
    return t

def t_TkNot(t):
    r'!'
    return t

def t_TkLeq(t):
    r'<='
    return t
    
def t_TkLess(t):
    r'<'
    return t


def t_TkGeq(t):
    r'>='
    return t

def t_TkGreater(t):
    r'>'
    return t

def t_TkEqual(t):
    r'=='
    return t

def t_TkNEqual(t):
    r'<>'
    return t

def t_TkOBracket(t):
    r'\['
    return t

def t_TkCBracket(t):
    r'\]'
    return t

def t_TkTwoPoints(t):
    r':'
    return t

def t_TkSoForth(t):
    r'\.\.'
    return t

def t_TkApp(t):
    r'\.'
    return t

t_ignore = ' \t'

def t_comment(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_TkString(t):
    #r'"([^\n\\"]|\\.)*"'
    r'"([^\n\\"]|\\["n\\])*"'
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
