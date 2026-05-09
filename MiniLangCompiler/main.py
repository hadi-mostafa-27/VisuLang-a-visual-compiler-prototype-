"""Command-line runner for the MiniLang compiler/interpreter used by VisuLang."""

import sys

from errors import LexicalError, MiniLangError, ParserError, RuntimeMiniLangError, SemanticError
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import (
    CodeOptimizer,
    IntermediateCodeGenerator,
    MachineCodeGenerator,
    format_numbered_lines,
)


def print_section(title):
    print(f"\n========== {title} ==========")


def run_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()
    except OSError as error:
        print(f"Could not read file: {error}")
        return 1

    print_section("SOURCE CODE")
    print(source_code)

    print_section("LEXICAL ANALYSIS")
    try:
        tokens = Lexer(source_code).scan_tokens()
        for token in tokens:
            print(token)
    except LexicalError as error:
        print(error)
        return 1

    print_section("SYNTAX ANALYSIS")
    try:
        ast = Parser(tokens).parse()
        print(ast)
    except ParserError as error:
        print(error)
        return 1

    print_section("SEMANTIC ANALYSIS")
    try:
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        print("Semantic analysis completed successfully.")
        print(semantic_analyzer.symbol_table_text())
    except SemanticError as error:
        print(error)
        return 1

    print_section("INTERMEDIATE CODE")
    intermediate_code = IntermediateCodeGenerator().generate(ast)
    print(format_numbered_lines(intermediate_code))

    print_section("OPTIMIZED CODE")
    optimized_code = CodeOptimizer().optimize(intermediate_code)
    print(format_numbered_lines(optimized_code))

    print_section("MACHINE LANGUAGE")
    machine_code = MachineCodeGenerator().generate(optimized_code)
    print(format_numbered_lines(machine_code))

    print_section("PROGRAM OUTPUT")
    try:
        interpreter = Interpreter()
        output = interpreter.interpret(ast)
        if output:
            print("\n".join(output))
        else:
            print("(program finished with no output)")
    except RuntimeMiniLangError as error:
        print(error)
        return 1

    return 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py examples/valid_program.minilang")
        return 1

    try:
        return run_file(sys.argv[1])
    except MiniLangError as error:
        print(error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
