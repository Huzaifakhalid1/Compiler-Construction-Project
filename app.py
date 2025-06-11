import streamlit as st
from parser import parser
from semantic import SymbolTable, check_semantics
from codegen import generate_python
from lexer import lexer
import io
import contextlib

st.title("Matrix DSL Compiler")

dsl_input = st.text_area("Enter your DSL code here:", height=200)

if st.button("Compile"):
    if dsl_input.strip() == "":
        st.warning("Please enter some DSL code.")
    else:
        # Lex and parse
        lexer.input(dsl_input)
        ast = parser.parse(dsl_input)
        
        if ast is None:
            st.error("Parsing failed. Please check your syntax.")
        else:
            try:
                # Semantic Analysis
                symtab = SymbolTable()
                check_semantics(ast, symtab)

                # Code Generation
                py_code = generate_python(ast)

                st.subheader("✅ Generated Python Code")
                st.code(py_code, language='python')

                # Execute the generated Python code
                namespace = {}
                with contextlib.redirect_stdout(io.StringIO()) as f:
                    exec(py_code, namespace)
                    output = f.getvalue()

                st.subheader("🧮 Output")
                st.text(output)

                # Show result variables if available
                display_vars = ['A', 'B', 'C_add', 'T', 'D_det', 'C_sub', 'C_div']
                for var in display_vars:
                    if var in namespace:
                        st.write(f"**{var} =**")
                        st.write(namespace[var])

            except Exception as e:
                st.error(f"Error during compilation: {e}")
