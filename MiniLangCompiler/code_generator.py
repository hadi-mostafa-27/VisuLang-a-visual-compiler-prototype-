"""Intermediate code, optimization, and toy machine code for MiniLang.

This module is intentionally simple and educational. It does not replace the
interpreter. Instead, it adds extra compiler-learning steps after semantic
analysis:

1. Generate three-address intermediate code.
2. Apply small optimizations such as constant folding.
3. Translate the optimized code into a tiny assembly-style machine language.
"""

from ast_nodes import (
    Assignment,
    BinaryExpression,
    Block,
    Declaration,
    Identifier,
    IfStatement,
    Literal,
    PrintStatement,
    Program,
    UnaryExpression,
    WhileStatement,
)


class IntermediateCodeGenerator:
    """Generate simple three-address code from the AST."""

    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self, program):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        self.visit(program)
        return list(self.instructions)

    def visit(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.visit(statement)
            return
        if isinstance(node, Block):
            for statement in node.statements:
                self.visit(statement)
            return
        if isinstance(node, Declaration):
            self.visit_declaration(node)
            return
        if isinstance(node, Assignment):
            value = self.expression(node.expression)
            self.emit(f"{node.name} = {value}")
            return
        if isinstance(node, PrintStatement):
            value = self.expression(node.expression)
            self.emit(f"PRINT {value}")
            return
        if isinstance(node, IfStatement):
            self.visit_if(node)
            return
        if isinstance(node, WhileStatement):
            self.visit_while(node)
            return

        raise ValueError(f"Cannot generate intermediate code for {type(node).__name__}")

    def visit_declaration(self, declaration):
        self.emit(f"DECLARE {declaration.var_type} {declaration.name}")
        if declaration.initializer is not None:
            value = self.expression(declaration.initializer)
            self.emit(f"{declaration.name} = {value}")

    def visit_if(self, if_statement):
        else_label = self.new_label()
        end_label = self.new_label()

        condition = self.expression(if_statement.condition)
        self.emit(f"IF_FALSE {condition} GOTO {else_label}")
        self.visit(if_statement.then_block)
        self.emit(f"GOTO {end_label}")
        self.emit(f"LABEL {else_label}")

        if if_statement.else_block is not None:
            self.visit(if_statement.else_block)

        self.emit(f"LABEL {end_label}")

    def visit_while(self, while_statement):
        start_label = self.new_label()
        end_label = self.new_label()

        self.emit(f"LABEL {start_label}")
        condition = self.expression(while_statement.condition)
        self.emit(f"IF_FALSE {condition} GOTO {end_label}")
        self.visit(while_statement.body)
        self.emit(f"GOTO {start_label}")
        self.emit(f"LABEL {end_label}")

    def expression(self, expression):
        if isinstance(expression, Literal):
            return self.format_literal(expression.value)
        if isinstance(expression, Identifier):
            return expression.name
        if isinstance(expression, UnaryExpression):
            value = self.expression(expression.expression)
            temp = self.new_temp()
            # Store unary minus as a normal binary instruction for easy codegen.
            self.emit(f"{temp} = 0 - {value}")
            return temp
        if isinstance(expression, BinaryExpression):
            left = self.expression(expression.left)
            right = self.expression(expression.right)
            temp = self.new_temp()
            self.emit(f"{temp} = {left} {expression.operator} {right}")
            return temp

        raise ValueError(f"Cannot generate expression code for {type(expression).__name__}")

    def emit(self, instruction):
        self.instructions.append(instruction)

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def format_literal(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


class CodeOptimizer:
    """Apply beginner-friendly optimizations to intermediate code."""

    def optimize(self, instructions):
        optimized = []
        for instruction in instructions:
            folded = self.fold_constants(instruction)
            if self.is_self_assignment(folded):
                continue
            optimized.append(folded)

        return self.remove_jump_to_next_label(optimized)

    def fold_constants(self, instruction):
        parts = instruction.split()
        if len(parts) != 5 or parts[1] != "=":
            return instruction

        target, _, left, operator, right = parts
        left_value = self.parse_literal(left)
        right_value = self.parse_literal(right)
        if left_value is None or right_value is None:
            return instruction

        result = self.evaluate_constant(left_value, operator, right_value)
        if result is None:
            return instruction

        return f"{target} = {self.format_literal(result)}"

    def parse_literal(self, text):
        if text == "true":
            return True
        if text == "false":
            return False
        if text.startswith("-") and text[1:].isdigit():
            return int(text)
        if text.isdigit():
            return int(text)
        return None

    def evaluate_constant(self, left, operator, right):
        if operator == "+" and isinstance(left, int) and isinstance(right, int):
            return left + right
        if operator == "-" and isinstance(left, int) and isinstance(right, int):
            return left - right
        if operator == "*" and isinstance(left, int) and isinstance(right, int):
            return left * right
        if operator == "/" and isinstance(left, int) and isinstance(right, int) and right != 0:
            return left // right
        if operator == "==" and type(left) is type(right):
            return left == right
        if operator == "!=" and type(left) is type(right):
            return left != right
        if operator == "<" and isinstance(left, int) and isinstance(right, int):
            return left < right
        if operator == ">" and isinstance(left, int) and isinstance(right, int):
            return left > right
        if operator == "<=" and isinstance(left, int) and isinstance(right, int):
            return left <= right
        if operator == ">=" and isinstance(left, int) and isinstance(right, int):
            return left >= right
        return None

    def is_self_assignment(self, instruction):
        parts = instruction.split()
        return len(parts) == 3 and parts[1] == "=" and parts[0] == parts[2]

    def remove_jump_to_next_label(self, instructions):
        cleaned = []
        for index, instruction in enumerate(instructions):
            parts = instruction.split()
            if (
                len(parts) == 2
                and parts[0] == "GOTO"
                and index + 1 < len(instructions)
                and instructions[index + 1] == f"LABEL {parts[1]}"
            ):
                continue
            cleaned.append(instruction)
        return cleaned

    def format_literal(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


class MachineCodeGenerator:
    """Translate optimized intermediate code to a tiny assembly-like language."""

    OPERATIONS = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        "==": "CMP_EQ",
        "!=": "CMP_NE",
        "<": "CMP_LT",
        ">": "CMP_GT",
        "<=": "CMP_LE",
        ">=": "CMP_GE",
    }

    def generate(self, instructions):
        machine_code = []
        for instruction in instructions:
            machine_code.extend(self.translate(instruction))
        return machine_code

    def translate(self, instruction):
        parts = instruction.split()
        if not parts:
            return []

        if parts[0] == "DECLARE" and len(parts) == 3:
            var_type, name = parts[1], parts[2]
            return [f"ALLOC {name} ; type {var_type}"]

        if parts[0] == "LABEL" and len(parts) == 2:
            return [f"{parts[1]}:"]

        if parts[0] == "GOTO" and len(parts) == 2:
            return [f"JMP {parts[1]}"]

        if parts[0] == "IF_FALSE" and len(parts) == 4 and parts[2] == "GOTO":
            condition, label = parts[1], parts[3]
            return [f"LOAD {condition}", f"JZ {label}"]

        if parts[0] == "PRINT" and len(parts) == 2:
            return [f"PRINT {parts[1]}"]

        if len(parts) == 3 and parts[1] == "=":
            target, source = parts[0], parts[2]
            return [f"LOAD {source}", f"STORE {target}"]

        if len(parts) == 5 and parts[1] == "=":
            target, left, operator, right = parts[0], parts[2], parts[3], parts[4]
            machine_operation = self.OPERATIONS.get(operator, "OP")
            return [f"LOAD {left}", f"{machine_operation} {right}", f"STORE {target}"]

        return [f"; Could not translate: {instruction}"]


def format_numbered_lines(lines):
    """Format generated code with line numbers for CLI and GUI display."""
    if not lines:
        return "(no code generated)"
    return "\n".join(f"{index + 1:02d}: {line}" for index, line in enumerate(lines))
