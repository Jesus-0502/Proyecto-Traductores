# Traductores e Interpretadores
# Etapa 2 del Proyecto
# Elaborado por: Mauricio Fragachan 20-10265
#                Jesus Gutierrez 20-10332

import sys
import ply.yacc as yacc
from lexer import tokens, lexer, find_column
import copy


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
# Tabla de Simbolos 
# ----------------------------

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}  # nombre -> tipo

    def declare(self, name, type_, lineno=None):
        if name in self.symbols:
            print(f"Variable {name} is already declared in the block at line {self.symbols[name][1]}")
            sys.exit(1)
        self.symbols[name] = (type_, lineno)

    def lookup(self, name, lineno=None, column=None):
        if name in self.symbols:
            return self.symbols[name][0]
        elif self.parent:
            return self.parent.lookup(name, lineno, column)
        else:
            print(f"Variable not declared at line {lineno} and column {column}")
            sys.exit(1)

    def print_table(self, indent=0):
        
        for name, type_ in self.symbols.items():
            if type_[0][0] != "function":
                print("-" * (indent) + f"variable: {name} | type: {type_[0]}")
            else:
                print("-" * (indent) + f"variable: {name} | type: {type_[0][0]}[..{type_[0][1]}]")
                
                
table = SymbolTable()

# ----------------------------
# -- Reglas del programa principal --
# ----------------------------

def p_program(p):
    '''program : TkOBlock declarations TkSemicolon instructions TkCBlock
                | TkOBlock instructions TkCBlock'''
    # global table
    # parent_table = copy.deepcopy(table)
    
    # # Crear nueva tabla de símbolos para este bloque
    # table = copy.deepcopy(SymbolTable(parent=parent_table))
    
    if len(p) == 6:
        p[0] = ("Block", ("Symbols Table", table), p[4])
    else:
        p[0] = ("Block", ("Symbols Table"), p[2])
        
    # table = parent_table
# ---------------------
# --- Declaraciones ---
# ---------------------

def p_declarations(p):
    '''declarations : declarations TkSemicolon declaration
                    | declaration'''

def p_declaration(p):
    '''declaration : TkInt idlist
                   | TkBool idlist
                   | TkFunction TkOBracket TkSoForth TkNum TkCBracket idlist'''
    if p[1] == 'int' or p[1] == 'bool':
        type = p[1]
        for var in p[2]:
            table.declare(var, type, p.lineno(1))
    else:
        type = (p[1], p[4])
        for var in p[6]:
            table.declare(var, type, p.lineno(1))

def p_idlist(p):
    '''idlist : idlist TkComma id
              | id'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]
        
def p_id(p):
    'id : TkId'
    p[0] = p[1]
        
def p_expression_list(p):
    '''expressionlist : expressionlist TkComma expression
                        | expression TkComma expression'''
    # if len(p) == 4:
        
    type = p[3][-1]
    if type != "int":
        print(f"There is no integer list at line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
        sys.exit(1)
        
    p[0] = ("Comma", p[1], p[3], "int") 

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
                    
    left_type = table.lookup(p[1], p.lineno(1), find_column(source_code, p.slice[1]))
    right_type = p[3][-1]
    # if left_type[0] == "function":
    #     if int(left_type[1]) + 1 != count_comma_elements(p[3]) and p[3][0] == "Comma":
    #         print(f"It is expected a list of length {left_type[1]} at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
    #         sys.exit(1)
    #     elif right_type != "function":
    #         print(f"Type error. Variable {p[1]} has different type than expression at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
    #         sys.exit(1)
    
    if left_type != right_type:    
        
        if left_type[0] == "function":
            
            if p[3][0] != "Comma" and right_type != "function":
                print(f"Type error. Variable {p[1]} has different type than expression at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
                sys.exit(1)
            
            elif int(left_type[1]) + 1 != count_comma_elements(p[3]) and p[3][0] == "Comma":
                print(f"It is expected a list of length {int(left_type[1]) + 1} at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
                sys.exit(1)
        
        elif right_type[0] == "function" and left_type != "function" and p.slice[3].type == "functionMod" :
            
            print(f"Variable {p[1]} is expected to be a function at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
            sys.exit(1)
        
        else:
            print(f"Type error. Variable {p[1]} has different type than expression at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
            sys.exit(1)
    elif p[3][0] == "Comma" and left_type == "int":
        print(f"Type error. Variable {p[1]} has different type than expression at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
        sys.exit(1)
        
    else:
        if  right_type[0] == "function" and left_type[0] == "function":
            if right_type[1] != left_type[1]:
                print(f"It is expected a list of length {left_type[1]} at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
                sys.exit(1)
    
    p[0] = ("Asig", ("Ident", p[1], left_type), p[3])

def p_print(p):
    '''print : TkPrint expression
             | TkPrint string'''
    p[0] = ("Print", p[2])

def p_skip(p):
    'skip : TkSkip'
    p[0] = ("skip",)

def p_while(p):
    'while : TkWhile expression TkArrow instructions TkEnd'
    
    type = p[2][-1]
    
    if type != "bool":
        print(f"No boolean guard at line {p.lineno(3)} and column {find_column(source_code, p.slice[3])}")
        sys.exit(1)
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
    
    type = p[1][-1]
    
    if type != "bool":
        print(f"No boolean guard at line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
        sys.exit(1)
    p[0] = ("Then", p[1], p[3])

# ------------------
# --- Operadores ---
# ------------------

def p_expression_binoperators(p: list):
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
                
    left_type = p[1][-1]
    right_type = p[3][-1]
    match p[2]:
        case '+':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Plus", p[1], p[3], "int")
        case '-':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Minus", p[1], p[3], "int")
        case '*':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Mult", p[1], p[3], "int")
        case '==':
            if left_type != right_type:
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Equal", p[1], p[3], "bool")
        case '<>':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("NotEqual", p[1], p[3], "bool")
        case '<':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Less", p[1], p[3], "bool")
        case '>':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Greater", p[1], p[3], "bool")
        case '>=':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Geq", p[1], p[3], "bool")
        case '<=':
            if left_type != "int" or right_type != "int":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Leq", p[1], p[3], "bool")
        case 'or':
            if left_type != "bool" or right_type != "bool":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("Or", p[1], p[3], "bool")
        case 'and':
            if left_type != "bool" or right_type != "bool":
                print(f"Type error in line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
                sys.exit(1)
            p[0] = ("And", p[1], p[3], "bool")

def p_expression_unoperators(p: list):
    '''expression : TkNot expression
                  | TkMinus expression %prec UMINUS'''
    right_type = p[2][-1]
    match p[1]:
        case '-':
            if right_type != "int":
                print(f"Type error in line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
                sys.exit(1)
            p[0] = ("Minus", p[2], "int")
        case '!':
            if right_type != "bool":
                print(f"Type error in line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
                sys.exit(1)
            p[0] = ("Not", p[2], "bool")

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
    
    left_type = table.lookup(p[1], p.lineno(1), find_column(source_code, p.slice[1]))
    right_type = p[3][-1]
    
    if left_type[0] != "function":
        print(f"Error. {p[1]} is not indexable at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
        sys.exit(1)
    
    if right_type != "int":
        print(f"Error. Not integer index for function at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
        sys.exit(1)
    
    p[0] = ("ReadFunction", ("Ident", p[1], left_type), p[3], "int")

def p_expression_function_app(p):
    'expression : functionMod TkApp expression'
    
    right_type = p[3][-1]
    
    if right_type != "int":
        (f"Error. Not integer index for function at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
    
    p[0] = ("ReadFunction", p[1], p[3], "int")

def p_function_mod(p):
    '''functionMod : functionMod TkOpenPar twopoints TkClosePar
                    | TkId TkOpenPar twopoints TkClosePar'''
                    
    
    if p.slice[1].type == 'functionMod':
        type = p[1][-1]
        p[0] = ("WriteFunction", p[1], p[3], type)
    else:
        type = table.lookup(p[1], p.lineno(1), find_column(source_code, p.slice[1]))
        if type[0] != "function":
            print(f"The function modification operator is use in not function variable at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
            sys.exit(1)
        p[0] = ("WriteFunction", ("Ident", p[1], type), p[3], type)


def p_twopoints(p):
    '''twopoints : expression TkTwoPoints expression'''
    
    left_type = p[1][-1]
    right_type = p[3][-1]
    if left_type != "int":
        print(f"Expected expression of type int at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) - 1}")
        sys.exit(1)
    if right_type != "int":
        print(f"Expected expression of type int at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
        sys.exit(1)
    
    p[0] = ("TwoPoints", p[1], p[3])
    

def p_expression_id(p):
    'expression : TkId'
    
    type = table.lookup(p[1], p.lineno(1), find_column(source_code, p.slice[1]))
    p[0] = ("Ident", p[1], type)
    

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
    p[0] = ("Concat", p[1], p[3])

def p_expression_literal(p):
    '''expression : TkNum
                  | TkTrue
                  | TkFalse'''
    t = p.slice[1].type
    if t == "TkTrue":
        p[0] = ("Literal", p[1], "bool")
    elif t == "TkFalse":
        p[0] = ("Literal", p[1], "bool")
    else:
        p[0] = ("Literal", p[1], "int")
# -----------------------
# --- Vacío y errores ---
# -----------------------

def p_error(p):
    if p:
        print(f"Sintax error in row {p.lineno}, column {p.lexpos}: unexpected token '{p.value}'.")
    else:
        print("Syntax error: unexpected end of input.")
    sys.exit(1)

def count_comma_elements(node):
    """
    Recibe el nodo Comma y cuenta cuántos elementos tiene.
    """
    if isinstance(node, tuple) and node[0] == "Comma":
        return count_comma_elements(node[1]) + 1
    else:
        return 1

def check_type(node, expected, table):
    typ = get_type(node, table)
    # print(f"Checking type: {typ} against expected: {expected}")
    if typ != expected:
        print(f"Type error: expected {expected}")
        sys.exit(1)

def get_type(node, table):
    # print(f"Getting type for node: {node}")
    if isinstance(node, str):
        if "| type: " in node:
            # print(f"Identified type: {node.split('| type: ')[-1]}")
            return node.split("| type: ")[-1]
    elif isinstance(node, tuple):
        return get_type(node[0], table)
        
    # print(f"Node type not recognized: {node}")
    return None


operators = ["Plus", "Minus", "Mult", "Equal", "NotEqual", "Leq", "Less", "Geq", "Greater", "And", "Or", "Not", "ReadFunction"]

def print_ast(ast, indent=0):
    if isinstance(ast, tuple):
        
        match ast[0]:
            case 'Literal':
                print(f"{"-" * indent}Literal: {ast[1]} | type: {ast[-1]}")
            
            case 'Ident':
                
                if ast[-1][0] == "function":
                    print(f"{"-" * indent}Ident: {ast[1]} | type: {ast[-1][0]}[..{ast[-1][1]}]")
                else:
                    print(f"{"-" * indent}Ident: {ast[1]} | type: {ast[-1]}")
            
            case operator if operator in operators:
                print(f"{"-" * indent}{operator} | type: {ast[-1]}")
                
                for child in ast[1:-1]:
                    print_ast(child, indent+1)
                
            case _:
                print("-" * indent + str(ast[0]))
                for child in ast[1:]:
                    print_ast(child, indent+1)
    elif isinstance(ast, SymbolTable):
        ast.print_table(indent)
    else:
        print("-" * indent + str(ast))

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

    #print("\n--- Análisis de contexto ---")
    #decorated = context_analysis(result)
    #print("\n--- AST Decorado ---")
    #print_ast(decorated)