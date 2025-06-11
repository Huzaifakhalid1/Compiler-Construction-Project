from parser import Transpose, Determinant

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, value):
        self.symbols[name] = value

    def lookup(self, name):
        shape = self.symbols.get(name)
        if shape is None:
            raise Exception(f"Undeclared variable: {name}")
        return shape

def check_semantics(ast, symtab):
    for stmt in ast.statements:
        if isinstance(stmt.expr, list):
            # Matrix literal: infer shape from nested list
            row_lengths = [len(row) for row in stmt.expr]
            assert all(l == row_lengths[0] for l in row_lengths), "Rows have inconsistent lengths"
            shape = (len(stmt.expr), row_lengths[0])
            symtab.declare(stmt.id, shape)

        elif hasattr(stmt.expr, 'left') and hasattr(stmt.expr, 'right'):
            # Binary operation: Addition or Multiplication
            lshape = symtab.lookup(stmt.expr.left)
            rshape = symtab.lookup(stmt.expr.right)
            if stmt.expr.op == '+':
                assert lshape == rshape, f"Addition shape mismatch: {lshape} vs {rshape}"
                symtab.declare(stmt.id, lshape)
            elif stmt.expr.op == '*':
                assert lshape[1] == rshape[0], f"Multiplication shape mismatch: {lshape} vs {rshape}"
                result_shape = (lshape[0], rshape[1])
                symtab.declare(stmt.id, result_shape)

        elif hasattr(stmt.expr, 'matrix'):
            # Unary operations: Transpose or Determinant
            shape = symtab.lookup(stmt.expr.matrix)
            if isinstance(stmt.expr, Transpose):
                symtab.declare(stmt.id, (shape[1], shape[0]))
            elif isinstance(stmt.expr, Determinant):
                assert shape[0] == shape[1], f"Determinant requires a square matrix, got shape {shape}"
                symtab.declare(stmt.id, (1, 1))
