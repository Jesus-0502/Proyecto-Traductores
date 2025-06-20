# Traductores e Interpretadores
# Etapa 2 del Proyecto
# Elaborado por: Mauricio Fragachan 20-10265
#                Jesus Gutierrez 20-10332

import sys
import ply.yacc as yacc
from lexer import tokens, lexer


# -------------------------
# - Reglas de precedencia -
# -------------------------
precedence = (
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('left', 'TkEqual', 'TkNEqual'),
    ('nonassoc', 'TkLess', 'TkLeq', 'TkGreater', 'TkGeq'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult'),
    ('nonassoc', 'TkApp'),
    ('right', 'TkNot'),
    ('right', 'UMINUS')
)

# ----------------------------
# -- Reglas del programa principal --
# ----------------------------

def p_program(p):
    '''program : TkOBlock declarations TkSemicolon instructions TkCBlock
                | TkOBlock instructions TkCBlock'''
    if len(p) == 6:
        p[0] = ("Block", ("Declare", p[2]), p[4])
    else:
        p[0] = ("Block", p[2])

# ---------------------
# --- Declaraciones ---
# ---------------------

def p_declarations(p):
    '''declarations : declarations TkSemicolon declaration
                    | declaration'''
    if len(p) == 4:
        p[0] = ("Sequencing", p[1], p[3])
    else:
        p[0] = p[1]

def p_declaration(p):
    '''declaration : TkInt idlist
                   | TkBool idlist
                   | TkFunction TkOBracket TkSoForth TkNum TkCBracket idlist'''
    if p[1] == 'int' or p[1] == 'bool':
        p[0] = f"{p[2]} : {p[1]}"
    else:
        p[0] = f"{p[6]} : function[..Literal: {p[4]}]"

def p_idlist(p):
    '''idlist : idlist TkComma id
              | id'''
    if len(p) == 4:
        p[0] = f"{p[1]}, {p[3]}"
    else:
        p[0] = p[1]
        
def p_id(p):
    'id : TkId'
    p[0] = p[1]
        
def p_expression_list(p):
    '''expressionlist : expressionlist TkComma expression
                        | expression TkComma expression'''
    if len(p) == 4:
        p[0] = ("Comma", p[1], p[3]) 

# ---------------------
# --- Instrucciones ---
# ---------------------

def p_instructions(p):
    '''instructions : instructions TkSemicolon instruction
                    | instruction'''
    if len(p) == 4:
        p[0] = ("Sequencing", p[1], p[3])
    else:
        p[0] = p[1]

def p_instruction(p):
    '''instruction : while
                   | if
                   | print
                   | skip
                   | program'''
    p[0] = p[1]

def p_assignment(p):
    '''instruction : TkId TkAsig expression
                    | TkId TkAsig expressionlist
                    | TkId TkAsig functionMod'''
    p[0] = ("Asig", ("Ident: " + p[1]), p[3])

def p_print(p):
    '''print : TkPrint expression
             | TkPrint string'''
    p[0] = ("Print", p[2])

def p_skip(p):
    'skip : TkSkip'
    p[0] = ("skip",)

def p_while(p):
    'while : TkWhile expression TkArrow instructions TkEnd'
    p[0] = ("While", ("Then", p[2], p[4]))

def p_if(p):
    'if : TkIf guardlist TkFi'
    p[0] = ("If", p[2])

def p_guardlist(p):
    '''guardlist : guardlist TkGuard guard
                 | guard'''
    if len(p) == 4:
        p[0] = ("Guard", p[1], p[3])
    else:
        p[0] = p[1]

def p_guard(p):
    'guard : expression TkArrow instructions'
    p[0] = ("Then", p[1], p[3])

# ------------------
# --- Operadores ---
# ------------------

def p_expression_binoperators(p):
    '''expression : expression TkPlus expression
                | expression TkMinus expression
                | expression TkMult expression
                | expression TkLeq expression
                | expression TkGeq expression
                | expression TkLess expression
                | expression TkGreater expression
                | expression TkEqual expression
                | expression TkNEqual expression
                | expression TkOr expression
                | expression TkAnd expression'''
    match p[2]:
        case '+':
            p[0] = ("Plus", p[1], p[3])
        case '-':
            p[0] = ("Minus", p[1], p[3])
        case '*':
            p[0] = ("Mult", p[1], p[3])
        case '==':
            p[0] = ("Equal", p[1], p[3])
        case '<>':
            p[0] = ("NotEqual", p[1], p[3])
        case '<':
            p[0] = ("Less", p[1], p[3])
        case '>':
            p[0] = ("Greater", p[1], p[3])
        case '>=':
            p[0] = ("Geq", p[1], p[3])
        case '<=':
            p[0] = ("Leq", p[1], p[3])
        case 'or':
            p[0] = ("Or", p[1], p[3])
        case 'and':
            p[0] = ("And", p[1], p[3])

def p_expression_unoperators(p):
    '''expression : TkNot expression
                  | TkMinus expression %prec UMINUS'''
    match p[1]:
        case '-':
            p[0] = ("Minus", p[2])
        case '!':
            p[0] = ("Not", p[2])

# ----------------------------------------
# - Definicion y asignacion de funciones -
# ----------------------------------------
def p_expression_dotaccess(p):
    '''expression : expression TkApp TkId
                  | expression TkApp TkNum'''
    token_type = p.slice[3].type
    if token_type == 'TkId':
        p[0] = ("App", p[1], ("Ident: " + p[3]))
    else: 
        p[0] = ("App", p[1], ("Literal: "+ p[3]))
        
def p_expression_app(p):
    'expression : TkId TkApp expression'
    p[0] = ("App", "Ident: " + p[1], p[3])

def p_expression_function_app(p):
    'expression : functionMod TkApp expression'
    p[0] = ("App", p[1], p[3])

def p_function_mod(p):
    '''functionMod : functionMod TkOpenPar twopoints TkClosePar
                    | TkId TkOpenPar twopoints TkClosePar'''
    if p.slice[1].type == 'functionMod':
        p[0] = ("WriteFunction", p[1], p[3])
    else:
        p[0] = ("WriteFunction", "Ident: " + p[1], p[3])


def p_twopoints(p):
    '''twopoints : expression TkTwoPoints expression'''
    p[0] = ("TwoPoints", p[1], p[3])
    

def p_expression_id(p):
    'expression : TkId'
    p[0] = "Ident: " + p[1]
    

def p_expression_par(p):
    'expression : TkOpenPar expression TkClosePar'
    p[0] = p[2]

# -----------------------    
# - Strings y Literales -
# -----------------------
    
def p_type_string(p):
    'string : TkString' 
    p[0] = ("String: " + p[1])
        
def p_sum_string(p):
    '''string : string TkPlus string
                | expression TkPlus string
                | string TkPlus expression'''
    p[0] = ("Plus", p[1], p[3])

def p_expression_literal(p):
    '''expression : TkNum
                  | TkTrue
                  | TkFalse'''
    t = p.slice[1].type
    if t == "TkTrue":
        p[0] = ("Literal: " + p[1])
    elif t == "TkFalse":
        p[0] = ("Literal: " + p[1])
    else:
        p[0] = ("Literal: "+ p[1])
# -----------------------
# --- Vacío y errores ---
# -----------------------

def p_error(p):
    if p:
        print(f"Sintax error in row {p.lineno}, column {p.lexpos}: unexpected token '{p.value}'.")
    else:
        print("Syntax error: unexpected end of input.")
    sys.exit(1)
    
# -----------------------
# - Impresión del árbol -
# -----------------------

def print_ast(tree, indent=0):
    if isinstance(tree, tuple):
        print("-" * indent + str(tree[0]))
        for child in tree[1:]:
            print_ast(child, indent + 1)
    else:
        print("-" * indent + str(tree))

# -----------------------
# - Ejecucion principal -
# -----------------------

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python parser.py <archivo.imperat>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        source_code = f.read()

    parser = yacc.yacc()
    result = parser.parse(source_code, lexer=lexer)
    print_ast(result)