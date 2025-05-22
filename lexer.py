import sys
import os
import ply.lex as lex
from utils import find_column, print_error
from tokens import *

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
            logs += f"{tok.type} (\"{tok.value}\") {tok.lineno} {find_column(data, tok)}\n"

    if has_error:
        sys.exit(1)
    else:
        print(logs)

if __name__ == "__main__":
    main()
