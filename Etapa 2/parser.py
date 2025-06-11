# Traductores e Interpretadores
# Etapa 2 del Proyecto
# Elaborado por: Mauricio Fragachan 20-10265
#                Jesus Gutierrez 20-10332

import ply.yacc as yacc
from lexer import tokens

# Operadores unarios
def p_expression_unoperators(p):
    '''expression: TkNot expression
                TkMinus expression'''
    match p[1]:
        case '!':
            p[0] = not p[2]
        case '-':
            p[0] = -p[2]

# Operadores binarios
def p_expression_binoperators(p):
    '''expression: expression TkPlus expression
                expression TkMinus expression
                expression TkMult expression
                expression TkLeq expression
                expression TkGeq expression
                expression TkLess expression
                expression TkGreater expression
                expression TkEqual expression
                expression TkNEqual expression
                expression TkOr expression
                expression TkAnd expression'''
    match p[2]:
        case '+':
            p[0] = p[1] + p[3]
        case '-':
            p[0] = p[1] - p[3]
        case '*':
            p[0] = p[1]*p[3]
        case '<':
            p[0] = p[1] < p[3]
        case '>':
            p[0] = p[1] > p[3]
        case '>=':
            p[0] = p[1] >= p[3]
        case '<=':
            p[0] = p[1] <= p[3]
        case '==':
            p[0] = p[1] == p[3]
        case '<>':
            p[0] = p[1] != p[3]
        case 'or':
            p[0] = p[1] or p[3]
        case 'and':
            p[0] = p[1] and p[3]

# Print
def p_statement_print(p): 
    '''statement: TkPrint expression 
                TkPrint TkString'''
    p[0] = p[3]
    
