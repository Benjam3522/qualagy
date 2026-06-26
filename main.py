from lexer import lex
from parser import Parser

code = """
var x = 5 + 2 * 3

if x > 10 { 
    write("x is greater than 10") 
} 
else { 
    write("x is less than or equal to 10") 
}
"""

tokens = lex(code)
parser = Parser(tokens)
ast = parser.parse()

print(ast)