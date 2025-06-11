import ply.lex as lex

reserved = {
    'matrix': 'MATRIX',
    'scalar': 'SCALAR',
    'TRANSPOSE': 'TRANSPOSE',
    'DETERMINANT': 'DETERMINANT'
}

tokens = [
    'ID', 'NUM', 'EQUALS', 'PLUS', 'TIMES','MINUS', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON'
] + list(reserved.values())



t_PLUS = r'\+'
t_TIMES = r'\*'
t_EQUALS = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_MINUS = r'-'
t_DIVIDE = r'/'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

