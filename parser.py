import ply.yacc as yacc
from lexer import tokens


class AST:
    def __init__(self):
        self.statements = []


class Statement:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Transpose:
    def __init__(self, matrix):
        self.matrix = matrix


class Determinant:
    def __init__(self, matrix):
        self.matrix = matrix


def p_program(p):
    'program : statement_list'
    p[0] = AST()
    p[0].statements = p[1]


def p_statement_list(p):
    '''statement_list : statement statement_list
                     | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_statement_matrix(p):
    'statement : MATRIX ID EQUALS matrix SEMICOLON'
    p[0] = Statement(p[2], p[4])


def p_statement_op(p):
    'statement : MATRIX ID EQUALS ID op ID SEMICOLON'
    p[0] = Statement(p[2], BinOp(p[4], p[5], p[6]))


def p_op(p):
    '''op : PLUS
          | MINUS
          | TIMES
          | DIVIDE'''
    p[0] = p[1]


def p_statement_transpose(p):
    'statement : MATRIX ID EQUALS TRANSPOSE LPAREN ID RPAREN SEMICOLON'
    p[0] = Statement(p[2], Transpose(p[6]))


def p_statement_determinant(p):
    'statement : MATRIX ID EQUALS DETERMINANT LPAREN ID RPAREN SEMICOLON'
    p[0] = Statement(p[2], Determinant(p[6]))


def p_statement_scalar_determinant(p):
    'statement : SCALAR ID EQUALS DETERMINANT LPAREN ID RPAREN SEMICOLON'
    p[0] = Statement(p[2], Determinant(p[6]))


def p_matrix(p):
    'matrix : LBRACKET row_list RBRACKET'
    p[0] = p[2]


def p_row_list(p):
    '''row_list : row COMMA row_list
               | row'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_row(p):
    'row : LBRACKET num_list RBRACKET'
    p[0] = p[2]


def p_num_list(p):
    '''num_list : NUM COMMA num_list
               | NUM'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()