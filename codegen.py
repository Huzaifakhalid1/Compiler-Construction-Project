import numpy as np
from parser import Transpose, Determinant  # ← this resolves the yellow warning

def generate_python(ast):
    code = ["import numpy as np"]
    for stmt in ast.statements:
        if isinstance(stmt.expr, list):
            code.append(f"{stmt.id} = np.array({stmt.expr})")
        elif hasattr(stmt.expr, 'left'):
            op = '+' if stmt.expr.op == '+' else '@'
            code.append(f"{stmt.id} = {stmt.expr.left} {op} {stmt.expr.right}")
        elif hasattr(stmt.expr, 'matrix'):
            if isinstance(stmt.expr, Transpose):
                code.append(f"{stmt.id} = {stmt.expr.matrix}.T")
            elif isinstance(stmt.expr, Determinant):
                code.append(f"{stmt.id} = np.linalg.det({stmt.expr.matrix})")
    return '\n'.join(code)
