from lexer import lex
from parser import Parser
from interpreter import Interpreter

code = """
var x = 5 + 2 * 3

if x > 10 {
    write("x is greater than 10")
}
else {
    write("x is less than or equal to 10")
}
"""

# 1. Lexing
tokens = lex(code)

print("=== TOKENS ===")
for token in tokens:
    print(token)

# 2. Parsing
parser = Parser(tokens)
ast = parser.parse()

print("\n=== AST ===")
for node in ast:
    print(node)

# 3. Interpreting
print("\n=== OUTPUT ===")
interpreter = Interpreter()
interpreter.execute(ast)