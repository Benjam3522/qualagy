from pathlib import Path

from lexer import lex
from parser import Parser
from interpreter import Interpreter

program_path = Path(__file__).with_name("program.txt")
code = program_path.read_text(encoding="utf-8")

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