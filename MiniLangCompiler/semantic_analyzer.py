"""Semantic analyzer for MiniLang.

This phase checks meaning, not just grammar. It verifies declarations,
types, assignment compatibility, and control-flow conditions.
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
from errors import SemanticError


class SemanticAnalyzer:
    def __init__(self):
        # Each dictionary is one scope. The first scope is the global scope.
        self.scopes = [{}]

    def analyze(self, program):
        self.visit(program)
        return True

    def visit(self, node):
        if isinstance(node, Program):
            return self.visit_program(node)
        if isinstance(node, Block):
            return self.visit_block(node)
        if isinstance(node, Declaration):
            return self.visit_declaration(node)
        if isinstance(node, Assignment):
            return self.visit_assignment(node)
        if isinstance(node, PrintStatement):
            return self.visit_print(node)
        if isinstance(node, IfStatement):
            return self.visit_if(node)
        if isinstance(node, WhileStatement):
            return self.visit_while(node)

        raise SemanticError(f"Unknown AST node: {type(node).__name__}")

    def visit_program(self, program):
        for statement in program.statements:
            self.visit(statement)

    def visit_block(self, block):
        self.begin_scope()
        try:
            for statement in block.statements:
                self.visit(statement)
        finally:
            self.end_scope()

    def visit_declaration(self, declaration):
        if declaration.name in self.current_scope():
            raise SemanticError(
                f"Variable '{declaration.name}' already declared in this scope",
                suggestion="Use a different variable name or remove the repeated declaration.",
            )

        if declaration.initializer is not None:
            initializer_type = self.check_expression(declaration.initializer)
            if initializer_type != declaration.var_type:
                raise SemanticError(
                    f"Cannot assign {initializer_type} value to {declaration.var_type} variable '{declaration.name}'",
                    suggestion=f"Use {self.type_phrase(declaration.var_type)} expression or change the variable type.",
                )

        self.current_scope()[declaration.name] = declaration.var_type

    def visit_assignment(self, assignment):
        variable_type = self.lookup_variable(assignment.name)
        value_type = self.check_expression(assignment.expression)

        if variable_type != value_type:
            raise SemanticError(
                f"Cannot assign {value_type} value to {variable_type} variable '{assignment.name}'",
                suggestion=f"Assign {self.type_phrase(variable_type)} expression to '{assignment.name}'.",
            )

    def visit_print(self, print_statement):
        value_type = self.check_expression(print_statement.expression)
        if value_type not in ("int", "bool"):
            raise SemanticError(
                "Print can only display int or bool values",
                suggestion="Print a variable, integer expression, boolean expression, true, or false.",
            )

    def visit_if(self, if_statement):
        condition_type = self.check_expression(if_statement.condition)
        if condition_type != "bool":
            raise SemanticError(
                "If condition must be boolean",
                suggestion="Use a comparison such as result > 20 or a bool variable.",
            )

        self.visit(if_statement.then_block)
        if if_statement.else_block is not None:
            self.visit(if_statement.else_block)

    def visit_while(self, while_statement):
        condition_type = self.check_expression(while_statement.condition)
        if condition_type != "bool":
            raise SemanticError(
                "While condition must be boolean",
                suggestion="Use a comparison such as x < 10 or a bool variable.",
            )

        self.visit(while_statement.body)

    def check_expression(self, expression):
        if isinstance(expression, Literal):
            return expression.value_type
        if isinstance(expression, Identifier):
            return self.lookup_variable(expression.name)
        if isinstance(expression, UnaryExpression):
            operand_type = self.check_expression(expression.expression)
            if expression.operator == "-" and operand_type == "int":
                return "int"
            raise SemanticError(
                "Unary '-' operator only works with integers",
                suggestion="Use '-' only before an integer expression.",
            )
        if isinstance(expression, BinaryExpression):
            return self.check_binary_expression(expression)

        raise SemanticError(f"Unknown expression: {type(expression).__name__}")

    def check_binary_expression(self, expression):
        left_type = self.check_expression(expression.left)
        right_type = self.check_expression(expression.right)
        operator = expression.operator

        if operator in ("+", "-", "*", "/"):
            if left_type == "int" and right_type == "int":
                return "int"
            raise SemanticError(
                f"Arithmetic operator '{operator}' only works with integers",
                suggestion="Use arithmetic operators only with int values.",
            )

        if operator in ("<", ">", "<=", ">="):
            if left_type == "int" and right_type == "int":
                return "bool"
            raise SemanticError(
                f"Comparison operator '{operator}' only works with integers",
                suggestion="Compare int expressions, for example: age >= 18.",
            )

        if operator in ("==", "!="):
            if left_type == right_type:
                return "bool"
            raise SemanticError(
                "Equality operators require both sides to have the same type",
                suggestion="Compare int with int, or bool with bool.",
            )

        raise SemanticError(f"Unknown operator '{operator}'", suggestion="Use a supported MiniLang operator.")

    def lookup_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(
            f"Variable '{name}' used before declaration",
            suggestion=f"Declare it first, for example: int {name};",
        )

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1]

    def symbol_table_text(self):
        lines = ["Symbol Table:"]
        if not self.scopes[0]:
            lines.append("  (empty)")
        else:
            for name, var_type in self.scopes[0].items():
                lines.append(f"  {name} : {var_type}")
        return "\n".join(lines)

    def symbol_table_rows(self):
        """Return rows that the GUI can show in a Treeview."""
        return [(name, var_type) for name, var_type in self.scopes[0].items()]

    def type_phrase(self, var_type):
        article = "an" if var_type == "int" else "a"
        return f"{article} {var_type}"
