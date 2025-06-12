# Traductores e Interpretadores
# Etapa 2 del Proyecto
# Elaborado por: Mauricio Fragachan 20-10265
#                Jesus Gutierrez 20-10332

import ply.yacc as yacc
from lexer import tokens, lexer

def p_program(p):
    'program : TkOBlock declarationlist TkSemicolon instructionlist TkCBlock'
    p[0] = ("Block" , ("Declare" , p[2]), p[4])


def p_declarationlist(p):
    ''' declarationlist : declarationlist TkSemicolon declaration
                        | declaration '''
    if len(p) == 4:
        p[0] = ( "Sequencing" , p[1] , p[3] )
    else:
        p[0] = p[1]

def p_declaration(p):
    ''' declaration : TkInt idlist
                    | TkBool idlist''' 
    p[0] = (p[2] + " : " +  p[1])
    
def p_idlist(p):
    ''' idlist : idlist TkComma TkId
                        | TkId '''
    if len(p) == 4:
        p[0] = ( p[3] + p[2] + " " + p[1] )
    else:
        p[0] = p[1]
    
def p_instructionlist(p):
    '''instructionlist : instructionlist TkSemicolon instruction
                        | instruction'''
    if len(p) == 4:
        p[0] = ( "Sequencing" , p[1] , p[3] )
    else:
        p[0] = p[1]
    
def p_instruction(p):
    'instruction : TkId TkAsig TkNum'
    p[0]
    p[0] = p[1] + " " + p[2] + " " + p[3]

# Operadores unarios
# def p_expression_unoperators(p):
#     '''expression: TkNot expression
#                 | TkMinus expression'''
#     match p[1]:
#         case '!':
#             p[0] = not p[2]
#         case '-':
#             p[0] = -p[2]

# Operadores binarios
# def p_expression_binoperators(p):
#     '''expression: expression TkPlus expression
#                 | expression TkMinus expression
#                 | expression TkMult expression
#                 | expression TkLeq expression
#                 | expression TkGeq expression
#                 | expression TkLess expression
#                 | expression TkGreater expression
#                 | expression TkEqual expression
#                 | expression TkNEqual expression
#                 | expression TkOr expression
#                 | expression TkAnd expression'''
#     match p[2]:
#         case '+':
#             p[0] = p[1] + p[3]
#         case '-':
#             p[0] = p[1] - p[3]
#         case '*':
#             p[0] = p[1]*p[3]
#         case '<':
#             p[0] = p[1] < p[3]
#         case '>':
#             p[0] = p[1] > p[3]
#         case '>=':
#             p[0] = p[1] >= p[3]
#         case '<=':
#             p[0] = p[1] <= p[3]
#         case '==':
#             p[0] = p[1] == p[3]
#         case '<>':
#             p[0] = p[1] != p[3]
#         case 'or':
#             p[0] = p[1] or p[3]
#         case 'and':
#             p[0] = p[1] and p[3]

# Print
# def p_statement_print(p): 
#     '''statement: TkPrint expression 
#                 | TkPrint string'''
#     p[0] = p[3]

# Tipo String   
def p_type_string(p):
    '''string : string TkPlus TkString
                | TkString'''
    if len(p) == 4:
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1]

def p_error(p):
    if p:
        print(f"Sintax error at '{p.value}' (line {p.lineno})")
    else:
        print("Sintax error at the end of the file")


data = '{ int a; a := 50 }'

parser = yacc.yacc()
result = parser.parse(data, lexer=lexer)
print(result)