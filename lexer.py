import sys
import os
import ply.lex as lex

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

# Funcion para calcular la columna de un token
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Funcion para imprimir un error
def print_error(char, row, column):
    print(f"Error: Unexpected character \"{char}\" in row {row}, column {column}")

lexer = lex.lex()

def main():
    if len(sys.argv) != 2:
        print("Uso: lexer <archivo.imperat>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".imperat"):
        print("Error: el archivo debe tener extensión .imperat")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: archivo '{filename}' no encontrado.")
        sys.exit(1)

    lexer.input(data)
    has_error = False
    logs = ""
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == 'ERROR':
            print_error(tok.value, tok.lineno, find_column(data, tok))
            has_error = True
        else:
            match tok.type:
                case 'TkNum':
                    logs += f"{tok.type}({tok.value}) {tok.lineno} {find_column(data, tok)}\n"
                case 'TkId':
                    logs += f"{tok.type}(\"{tok.value}\") {tok.lineno} {find_column(data, tok)}\n"
                case 'TkString':
                    logs += f"{tok.type}(\"{tok.value}\") {tok.lineno} {find_column(data, tok)}\n"
                case _:
                    logs += f"{tok.type} {tok.lineno} {find_column(data, tok)}\n"
    if has_error:
        sys.exit(1)
    else:
        print(logs)

if __name__ == "__main__":
    main()
