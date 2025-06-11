import numpy as np
from parser import Transpose, Determinant  # ← resolves yellow warning

def generate_python(ast):
    code = ["import numpy as np"]
    for stmt in ast.statements:
        if isinstance(stmt.expr, list):
            code.append(f"{stmt.id} = np.array({stmt.expr})")
        elif hasattr(stmt.expr, 'left'):
            if stmt.expr.op == '+':
                code.append(f"{stmt.id} = np.add({stmt.expr.left}, {stmt.expr.right})")
            elif stmt.expr.op == '-':
                code.append(f"{stmt.id} = np.subtract({stmt.expr.left}, {stmt.expr.right})")
            elif stmt.expr.op == '*':
                code.append(f"{stmt.id} = np.matmul({stmt.expr.left}, {stmt.expr.right})")
            elif stmt.expr.op == '/':
                code.append(f"{stmt.id} = np.divide({stmt.expr.left}, {stmt.expr.right})")
        elif hasattr(stmt.expr, 'matrix'):
            if isinstance(stmt.expr, Transpose):
                code.append(f"{stmt.id} = {stmt.expr.matrix}.T")
            elif isinstance(stmt.expr, Determinant):
                code.append(f"{stmt.id} = np.linalg.det({stmt.expr.matrix})")
    return '\n'.join(code)
