from lexer import lexer
from parser import parser
from semantic import SymbolTable, check_semantics
from codegen import generate_python

# Read DSL source
with open("sample.dsl") as f:
    source = f.read()

print("=== DSL Source ===")
print(source)
print("==================")

# Print DSL code
print("Source DSL Code:")
print(source)

# Tokenize
print("=== Tokens ===")
lexer.input(source)
for tok in lexer:
    print(tok)
print("==============")

# Parse
ast = parser.parse(source)

if ast is None:
    print("Parsing failed. Exiting.")
    exit(1)

# Semantic checks
symtab = SymbolTable()
check_semantics(ast, symtab)

# Generate Python code
py_code = generate_python(ast)

# Inject print statements for each variable
from parser import Statement, BinOp, Transpose, Determinant  # reuse AST types

output_lines = []
for stmt in ast.statements:
    output_lines.append("")  # for spacing
    output_lines.append(f"# Output for {stmt.id}")
    if isinstance(stmt.expr, Determinant):
        output_lines.append(f"print('{stmt.id} =', {stmt.id})")
    else:
        output_lines.append(f"print('{stmt.id} =')")
        output_lines.append(f"for row in {stmt.id}: print(row)")

# Combine code and output
full_code = py_code + "\n\n" + "\n".join(output_lines)

# Save to output.py
with open("output.py", "w") as out:
    out.write(full_code)

print("Generated Python code saved to output.py")
