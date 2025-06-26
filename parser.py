import ply.lex as lex
import ply.yacc as yacc

# ------------------------------------
# LEXER
# ------------------------------------
tokens = (
    'ID', 'NUM',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS',
    'LBRACKET', 'RBRACKET',
    'LPAREN', 'RPAREN',
    'COMMA', 'SEMICOLON',
    'MATRIX', 'SCALAR',
    'TRANSPOSE', 'DETERMINANT'
)

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COMMA      = r','
t_SEMICOLON  = r';'

reserved = {
    'matrix': 'MATRIX',
    'scalar': 'SCALAR',
    'transpose': 'TRANSPOSE',
    'determinant': 'DETERMINANT'
}

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------------------------
# PARSE TREE NODE CLASS
# ------------------------------------
class ParseTreeNode:
    def __init__(self, label, children=None):  # ✅ fixed __init__
        self.label = label
        self.children = children if children is not None else []

    def to_dot(self, node_id=0, parent_id=None, lines=None):
        if lines is None:
            lines = ["digraph ParseTree {"]
        current_id = node_id
        lines.append(f'  node{current_id} [label="{self.label}"];')
        if parent_id is not None:
            lines.append(f'  node{parent_id} -> node{current_id};')
        next_id = current_id + 1
        for child in self.children:
            next_id = child.to_dot(next_id, current_id, lines)
        if parent_id is None:
            lines.append("}")
        return next_id if parent_id is not None else "\n".join(lines)

# ------------------------------------
# PARSER RULES
# ------------------------------------
def p_program(p):
    'program : statement_list'
    p[0] = ParseTreeNode("Program", [p[1]])

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = ParseTreeNode("StatementList", [p[1], p[2]])
    else:
        p[0] = ParseTreeNode("StatementList", [p[1]])

def p_statement_matrix(p):
    'statement : MATRIX ID EQUALS matrix SEMICOLON'
    p[0] = ParseTreeNode("Statement", [
        ParseTreeNode("MATRIX"),
        ParseTreeNode(f"ID: {p[2]}"),
        ParseTreeNode("="),
        p[4],
        ParseTreeNode(";")
    ])

def p_statement_op(p):
    'statement : MATRIX ID EQUALS ID op ID SEMICOLON'
    p[0] = ParseTreeNode("Statement", [
        ParseTreeNode("MATRIX"),
        ParseTreeNode(f"ID: {p[2]}"),
        ParseTreeNode("="),
        ParseTreeNode(f"ID: {p[4]}"),
        p[5],
        ParseTreeNode(f"ID: {p[6]}"),
        ParseTreeNode(";")
    ])

def p_op(p):
    '''op : PLUS
          | MINUS
          | TIMES
          | DIVIDE'''
    p[0] = ParseTreeNode(f"OP: {p[1]}")

def p_statement_transpose(p):
    'statement : MATRIX ID EQUALS TRANSPOSE LPAREN ID RPAREN SEMICOLON'
    p[0] = ParseTreeNode("Statement", [
        ParseTreeNode("MATRIX"),
        ParseTreeNode(f"ID: {p[2]}"),
        ParseTreeNode("="),
        ParseTreeNode("TRANSPOSE"),
        ParseTreeNode("("),
        ParseTreeNode(f"ID: {p[6]}"),
        ParseTreeNode(")"),
        ParseTreeNode(";")
    ])

def p_statement_determinant(p):
    'statement : MATRIX ID EQUALS DETERMINANT LPAREN ID RPAREN SEMICOLON'
    p[0] = ParseTreeNode("Statement", [
        ParseTreeNode("MATRIX"),
        ParseTreeNode(f"ID: {p[2]}"),
        ParseTreeNode("="),
        ParseTreeNode("DETERMINANT"),
        ParseTreeNode("("),
        ParseTreeNode(f"ID: {p[6]}"),
        ParseTreeNode(")"),
        ParseTreeNode(";")
    ])

def p_statement_scalar_determinant(p):
    'statement : SCALAR ID EQUALS DETERMINANT LPAREN ID RPAREN SEMICOLON'
    p[0] = ParseTreeNode("Statement", [
        ParseTreeNode("SCALAR"),
        ParseTreeNode(f"ID: {p[2]}"),
        ParseTreeNode("="),
        ParseTreeNode("DETERMINANT"),
        ParseTreeNode("("),
        ParseTreeNode(f"ID: {p[6]}"),
        ParseTreeNode(")"),
        ParseTreeNode(";")
    ])

def p_matrix(p):
    'matrix : LBRACKET row_list RBRACKET'
    p[0] = ParseTreeNode("Matrix", [p[2]])

def p_row_list(p):
    '''row_list : row COMMA row_list
                | row'''
    if len(p) == 4:
        p[0] = ParseTreeNode("RowList", [p[1], ParseTreeNode(","), p[3]])
    else:
        p[0] = ParseTreeNode("RowList", [p[1]])

def p_row(p):
    'row : LBRACKET num_list RBRACKET'
    p[0] = ParseTreeNode("Row", [ParseTreeNode("["), p[2], ParseTreeNode("]")])

def p_num_list(p):
    '''num_list : NUM COMMA num_list
                | NUM'''
    if len(p) == 4:
        p[0] = ParseTreeNode("NumList", [ParseTreeNode(f"NUM: {p[1]}"), ParseTreeNode(","), p[3]])
    else:
        p[0] = ParseTreeNode("NumList", [ParseTreeNode(f"NUM: {p[1]}")])

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ------------------------------------
# MAIN FUNCTION
# ------------------------------------
if __name__ == "__main__":  # ✅ fixed
    input_text = "matrix A = [[1,2],[3,4]];"
    result = parser.parse(input_text)

    if result:
        dot_output = result.to_dot()
        try:
            with open("parse_tree.dot", "w") as f:
                f.write(dot_output)
            print("Parse tree written to parse_tree.dot")
            print("You can render it using: dot -Tpng parse_tree.dot -o parse_tree.png")
        except Exception as e:
            print(f"Error writing DOT file: {e}")
    else:
        print("Parsing failed.")
