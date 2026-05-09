import os
import sys
import unittest


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from ast_nodes import Declaration, PrintStatement  # noqa: E402
from code_generator import CodeOptimizer, IntermediateCodeGenerator, MachineCodeGenerator  # noqa: E402
from errors import SemanticError  # noqa: E402
from interpreter import Interpreter  # noqa: E402
from lexer import Lexer  # noqa: E402
from parser import Parser  # noqa: E402
from semantic_analyzer import SemanticAnalyzer  # noqa: E402


def parse_source(source):
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()


class TestMiniLang(unittest.TestCase):
    def test_lexer_token_generation(self):
        tokens = Lexer("int x = 5; print(x);").scan_tokens()
        token_types = [token.token_type for token in tokens]

        self.assertEqual(
            token_types,
            [
                "INT",
                "IDENTIFIER",
                "ASSIGN",
                "INTEGER",
                "SEMICOLON",
                "PRINT",
                "LPAREN",
                "IDENTIFIER",
                "RPAREN",
                "SEMICOLON",
                "EOF",
            ],
        )

    def test_parser_ast_generation(self):
        ast = parse_source("int x = 5; print(x);")

        self.assertEqual(len(ast.statements), 2)
        self.assertIsInstance(ast.statements[0], Declaration)
        self.assertIsInstance(ast.statements[1], PrintStatement)

    def test_semantic_analyzer_detects_undeclared_variables(self):
        ast = parse_source("print(x);")

        with self.assertRaises(SemanticError):
            SemanticAnalyzer().analyze(ast)

    def test_semantic_analyzer_detects_wrong_assignment_type(self):
        ast = parse_source("int x; x = true;")

        with self.assertRaises(SemanticError):
            SemanticAnalyzer().analyze(ast)

    def test_interpreter_executes_print_statements(self):
        ast = parse_source("int x = 2; print(x + 3);")
        SemanticAnalyzer().analyze(ast)
        output = Interpreter().interpret(ast)

        self.assertEqual(output, ["5"])

    def test_interpreter_can_collect_execution_trace(self):
        ast = parse_source("int x = 2; x = x + 3; print(x);")
        SemanticAnalyzer().analyze(ast)
        interpreter = Interpreter(collect_trace=True)
        output = interpreter.interpret(ast)

        self.assertEqual(output, ["5"])
        self.assertIn("Declared variable x = 2", interpreter.trace)
        self.assertIn("Assigned x = 5", interpreter.trace)

    def test_code_generation_optimization_and_machine_language(self):
        ast = parse_source("int x = 5; int result; result = 10 * 2; print(result);")
        SemanticAnalyzer().analyze(ast)

        intermediate_code = IntermediateCodeGenerator().generate(ast)
        optimized_code = CodeOptimizer().optimize(intermediate_code)
        machine_code = MachineCodeGenerator().generate(optimized_code)

        self.assertIn("DECLARE int x", intermediate_code)
        self.assertIn("t1 = 10 * 2", intermediate_code)
        self.assertIn("t1 = 20", optimized_code)
        self.assertIn("ALLOC x ; type int", machine_code)
        self.assertIn("STORE result", machine_code)
        self.assertIn("PRINT result", machine_code)


if __name__ == "__main__":
    unittest.main()
