import sys
import os
import ply.lex as lex
#from utils import find_column, print_error
from tokens import *


def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

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
