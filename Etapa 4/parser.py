# Traductores e Interpretadores
# Etapa 3 del Proyecto
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
            print(f"Variable {name} not declared at line {lineno} and column {column}")
            sys.exit(1)

    def print_table(self, indent=0):
        
        for name, type_ in self.symbols.items():
            if type_[0][0] != "function":
                print("-" * (indent) + f"variable: {name} | type: {type_[0]}")
            else:
                print("-" * (indent) + f"variable: {name} | type: {type_[0][0]}[..{type_[0][1]}]")
                
# Tabla de Simbolos global       
global_table = SymbolTable()
table = global_table
# ----------------------------
# -- Reglas del programa principal --
# ----------------------------

def p_program(p):
    '''program : new_block declarations TkSemicolon instructions TkCBlock
                | new_block instructions TkCBlock'''
    global table
    
    if len(p) == 6:
        p[0] = ("Block", ("Symbols Table", table), p[4])
    else:
        p[0] = ("Block", ("Symbols Table"), p[2])
    table = table.parent
        
def p_new_block(p):
    '''new_block : TkOBlock'''
    global table
    
    new_table = SymbolTable(parent=table)
    table = new_table

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
    type = p[3][-1]
    if type != "int":
        print(f"There is no integer list at line {p.lineno(2)} and column {find_column(source_code, p.slice[2])}")
        sys.exit(1)
        
    p[0] = ("Comma", p[1], p[3], "int", count_comma_elements(p[1])) 

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

# Falta por pulir pero funciona por ahora
def p_assignment(p):
    '''instruction : TkId TkAsig expression
                    | TkId TkAsig expressionlist
                    | TkId TkAsig functionMod'''
                    
    left_type = table.lookup(p[1], p.lineno(1), find_column(source_code, p.slice[1]))
    right_type = p[3][-1]

    if left_type != right_type:    
        if left_type[0] != "function" or left_type[1] != "0" or right_type != "int":
        
            if left_type[0] == "function":
                
                if (p[3][0] != "Comma" and right_type != "function"):
                    print(f"Type error. Variable {p[1]} has different type than expression at line {p.lineno(1)} and column {find_column(source_code, p.slice[1])}")
                    sys.exit(1)
                
                elif int(left_type[1]) + 1 != count_comma_elements(p[3]) and p[3][0] == "Comma":
                    print(f"It is expected a list of length {int(left_type[1]) + 1} at line {p.lineno(2)} and column {find_column(source_code, p.slice[2]) + 1}")
                    sys.exit(1)
                
            elif p[3][-2] == "function" and left_type != "function" and p.slice[3].type == "functionMod" :
                
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
            if left_type != right_type:
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
    p[0] = ("Concat", p[1], p[3], "String")

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


operators = ["Plus", "Minus", "Mult", "Equal", "NotEqual", "Leq", "Less", "Geq", "Greater", "And", "Or", "Not", "ReadFunction", "WriteFunction", "Concat"]

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
                
                if operator == "WriteFunction":
                    print(f"{"-" * indent}{operator} | type: {ast[-1][0]}[..{ast[-1][1]}]")
                else:
                    print(f"{"-" * indent}{operator} | type: {ast[-1]}")
                    
                for child in ast[1:-1]:
                    print_ast(child, indent+1)

            case "Comma":
                print(f"{"-" * indent}Comma | type: function with length={int(ast[-1]) + 1}")
                for child in ast[1:-2]:
                    print_ast(child, indent + 1)
            
            case _:
                print("-" * indent + str(ast[0]))
                for child in ast[1:]:
                    print_ast(child, indent+1)
    elif isinstance(ast, SymbolTable):
        ast.print_table(indent)
    else:
        print("-" * indent + str(ast))


# Combinadores y primitivas según la Etapa 4
COMBINATORS = """
Z = lambda g:(lambda x:g(lambda v:x(x)(v)))(lambda x:g(lambda v:x(x)(v)))
true = lambda x:lambda y:x
false = lambda x:lambda y:y
nil = lambda x:true
cons = lambda x:lambda y:lambda f: f(x)(y)
head = lambda p: p(true)
tail = lambda p:p(false)
apply = Z(lambda g:lambda f:lambda x:f if x==nil else (g(f(head(x)))(tail(x))))
lift_do=lambda exp:lambda f:lambda g: lambda x: g(f(x)) if (exp(x)) else x
do=lambda exp:lambda f:Z(lift_do(exp)(f))
"""

def translate_to_lambda(ast):
    """
    Recibe el AST decorado y devuelve el código Python con:
    - combinadores
    - definición de program
    - llamada final a apply e impresión
    """
    var_names = extract_symbols(ast)
    print(var_names)
    

    # Recolectar las asignaciones en orden
    assignments = collect_assignments(ast)

    # Construir el cuerpo del program usando apply encadenados
    body = build_program_body(assignments, var_names)

    # Construir la lista inicial cons(0)(cons(0)...(nil))
    init_list = build_init_list(var_names)

    # Construir apply final para imprimir las variables
    apply_vars = ": lambda ".join(key for key,_ in reversed(var_names.items()))
    print_part = "{" + ", ".join([f"'{v}': {v}" for v in var_names]) + "}"

    final_code = f"""{COMBINATORS}

program = (lambda x1: {body})

result = program({init_list})
print(apply(lambda {apply_vars}: {print_part})(result))
"""
    return final_code

def collect_assignments(node):
    """
    Recoge todas las asignaciones (tuplas con tag 'Asig') en orden de aparición.
    """
    if isinstance(node, tuple):
        if node[0] == "Sequencing":
            return collect_assignments(node[1]) + collect_assignments(node[2])
        elif node[0] == "Asig":
            #print([node])
            return [node]
        elif node[0] == "Block":
            return collect_assignments(node[-1])
        else:
            return []
    return []

def build_program_body(assignments, var_names):
    """
    Construye apply(lambda...)(apply(lambda...)(initial))
    """
    n = len(var_names)
    print(var_names)
    acc = "x1"
    for asig in assignments:
        expr_node = asig[2]
        print(expr_node)
        expr_code = translate_expr(expr_node)
        print(expr_code)
        for key, value in var_names.items():
            if key in expr_code:
                expr_code = expr_code.replace(key, value[0])
            
        
        lam_vars = ": lambda ".join(f"{value[0]}" for _, value in reversed(var_names.items()))
        cons_chain = build_cons_chain(expr_code, asig, var_names)
        apply_part = f"(apply(lambda {lam_vars}: {cons_chain}))({acc})"
        acc = apply_part
    return acc

def build_cons_chain(expr_code, asig, var_names):
    """
    cons(xN)(cons(...)(cons(expr_code)(nil)))
    """
    
    var_change = asig[1][1]
    print("Esta es la variable a cambiar:", var_change)
    code = f"nil"
    for key, value in var_names.items():
        if isinstance(key, tuple):
            if key[0] == var_change:
                code = f"cons({expr_code})({code})"
            else:
                code = f"cons({value[0]})({code})"
            
        elif key == var_change:
            code = f"cons({expr_code})({code})"
        else:
            code = f"cons({value[0]})({code})"
        print(code)
    return code

def translate_expr(node):
    """
    Traduce una expresión a Python.
    """
    # if lista is None:
    #     lista = []
    
    if isinstance(node, tuple):
        tag = node[0]
        if tag == "Literal":
            return node[1]
        elif tag == "Ident":
            return node[1]
        elif tag in {"Plus", "Minus", "Mult", "Less", "Greater", "Leq", "Geq", "Equal", "NotEqual", "And", "Or, Not"}:
            if len(node) == 4:
                left = translate_expr(node[1])
                right = translate_expr(node[2])
                op = {
                    "Plus": "+", "Minus": "-", "Mult": "*",
                    "Less": "<", "Greater": ">", "Leq": "<=", "Geq": ">=",
                    "Equal": "==", "NotEqual": "!=", "And": "and", "Or": "or"
                }[tag]
                return f"{left}{op}{right}"
            else:
                child = translate_expr(node[1])
                return f"-{child}"
        elif tag == "Comma":
            left = translate_expr(node[1])
            right = translate_expr(node[2])
            result = []
            if left != "":
                result += [int(left)] if isinstance(left, str) else left
            if right != "":
                result += [int(right)] if isinstance(right, str) else right
            return result
        elif tag == "ReadFunction":
            ident = translate_expr(node[1])
            index = translate_expr(node[2])
            return f"{ident}[{index}]"
    return ""

def build_init_list(var_names):
    """
    cons(0)(cons(0)...(nil))
    """
    code = "nil"
    for key, value in var_names.items():
        if value[1] == "function":
            list = [] 
            for i in range(int(value[2])+1):
                list.append(0)
            code = f"cons({list})({code})"
        elif value[1] == "bool":        
            code = f"cons(False)({code})"
        else:
            code = f"cons(0)({code})"   
    return code

def extract_symbols(ast):
    """
    Extrae las variables declaradas del primer bloque.
    """
    var_names = {}
    i = 1
    if isinstance(ast, tuple) and ast[0] == "Block":
        symbols_node = ast[1]
        symbols_list = []
        if isinstance(symbols_node, tuple) and symbols_node[0] == "Symbols Table":
            table = symbols_node[1].symbols
            for name, type_ in table.items():
                if type_[0][0] != "function":
                    
                    symbols_list += [(name, type_[0])]
                    var_names[name] = (f"x{i}", type_[0] )

                else:
                    symbols_list += [(name, type_[0][1])]
                    var_names[name] = (f"x{i}", type_[0][0], type_[0][1])
                i += 1
                
            return var_names
    return {}

# -----------------------
# Ejecución principal
# -----------------------
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python translator.py <archivo.imperat> <salida.py>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, encoding="utf-8") as f:
        source_code = f.read()

    parser = yacc.yacc()
    result = parser.parse(source_code, lexer=lexer)

    # Si quieres ver el AST decorado:
    # print_ast(result)

    code = translate_to_lambda(result)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Archivo traducido generado en: {output_file}")