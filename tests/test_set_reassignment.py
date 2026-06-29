import io
import unittest
from contextlib import redirect_stdout

from interpreter import Interpreter
from lexer import lex
from parser import Parser, SetStmt


class SetReassignmentTests(unittest.TestCase):
    def test_set_reassigns_existing_variable(self):
        code = "var x = 1; set x = 10;"
        tokens = lex(code)
        ast = Parser(tokens).parse()

        self.assertEqual(len(ast), 2)
        self.assertIsInstance(ast[1], SetStmt)

        interpreter = Interpreter()
        interpreter.execute(ast)

        self.assertEqual(interpreter.variables["x"], 10.0)

    def test_log_write_statement_is_parsed_and_executed(self):
        code = 'log.write("hello");'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        self.assertEqual(len(ast), 1)

        interpreter = Interpreter()
        interpreter.execute(ast)

    def test_log_write_accepts_multiple_arguments(self):
        code = 'var x = 5; log.write("value: ", x);'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            Interpreter().execute(ast)

        self.assertIn("value: 5", buffer.getvalue())

    def test_multiple_log_write_calls_execute_in_sequence(self):
        code = 'log.write("first"); log.write("second");'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            Interpreter().execute(ast)

        self.assertIn("first", buffer.getvalue())
        self.assertIn("second", buffer.getvalue())

    def test_random_accepts_variable_bounds(self):
        code = 'var low = 2; var high = 5; var r = random(low, high);'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        interpreter = Interpreter()
        interpreter.execute(ast)

        self.assertIn("r", interpreter.variables)
        self.assertGreaterEqual(interpreter.variables["r"], 2)
        self.assertLessEqual(interpreter.variables["r"], 5)

    def test_change_is_alias_for_set(self):
        code = 'var x = 1; change x = 10;'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        interpreter = Interpreter()
        interpreter.execute(ast)

        self.assertEqual(interpreter.variables["x"], 10.0)

    def test_get_builtin_reads_existing_variable(self):
        code = 'var x = 7; var y = get("x");'
        tokens = lex(code)
        ast = Parser(tokens).parse()

        interpreter = Interpreter()
        interpreter.execute(ast)

        self.assertEqual(interpreter.variables["y"], 7.0)


if __name__ == "__main__":
    unittest.main()
