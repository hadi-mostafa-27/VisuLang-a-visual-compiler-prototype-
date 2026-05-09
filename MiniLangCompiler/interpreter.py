"""Tree-walking interpreter for MiniLang."""

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
from errors import RuntimeMiniLangError


class Interpreter:
    def __init__(self, collect_trace=False, trace_enabled=None):
        if trace_enabled is not None:
            collect_trace = trace_enabled
        self.scopes = [{}]
        self.output = []
        self.trace = []
        self.collect_trace = collect_trace
        self.max_loop_iterations = 10000

    def interpret(self, program):
        self.execute(program)
        return self.output

    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.execute(statement)
            return
        if isinstance(node, Block):
            self.execute_block(node)
            return
        if isinstance(node, Declaration):
            self.execute_declaration(node)
            return
        if isinstance(node, Assignment):
            self.execute_assignment(node)
            return
        if isinstance(node, PrintStatement):
            self.execute_print(node)
            return
        if isinstance(node, IfStatement):
            self.execute_if(node)
            return
        if isinstance(node, WhileStatement):
            self.execute_while(node)
            return

        raise RuntimeMiniLangError(f"Unknown AST node: {type(node).__name__}")

    def execute_block(self, block):
        self.add_trace("Entered a new block scope")
        self.begin_scope()
        try:
            for statement in block.statements:
                self.execute(statement)
        finally:
            self.end_scope()
            self.add_trace("Exited block scope")

    def execute_declaration(self, declaration):
        if declaration.initializer is None:
            value = 0 if declaration.var_type == "int" else False
        else:
            value = self.evaluate(declaration.initializer)
        self.current_scope()[declaration.name] = value
        self.add_trace(f"Declared variable {declaration.name} = {self.format_value(value)}")

    def execute_assignment(self, assignment):
        value = self.evaluate(assignment.expression)
        self.assign_variable(assignment.name, value)
        self.add_trace(f"Assigned {assignment.name} = {self.format_value(value)}")

    def execute_print(self, print_statement):
        value = self.evaluate(print_statement.expression)
        self.output.append(self.format_value(value))
        self.add_trace(f"Printed {self.format_value(value)}")

    def execute_if(self, if_statement):
        condition_value = self.evaluate(if_statement.condition)
        self.add_trace(
            f"Condition {if_statement.condition.to_source()} evaluated to {self.format_value(condition_value)}"
        )
        if condition_value:
            self.execute(if_statement.then_block)
        elif if_statement.else_block is not None:
            self.execute(if_statement.else_block)

    def execute_while(self, while_statement):
        iterations = 0
        while True:
            condition_value = self.evaluate(while_statement.condition)
            self.add_trace(
                f"While condition {while_statement.condition.to_source()} evaluated to {self.format_value(condition_value)}"
            )
            if not condition_value:
                break
            iterations += 1
            if iterations > self.max_loop_iterations:
                raise RuntimeMiniLangError(
                    "Loop stopped because it may be infinite",
                    suggestion="Check that the while loop condition eventually becomes false.",
                )
            self.execute(while_statement.body)

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        if isinstance(expression, Identifier):
            return self.get_variable(expression.name)
        if isinstance(expression, UnaryExpression):
            value = self.evaluate(expression.expression)
            if expression.operator == "-":
                return -value
        if isinstance(expression, BinaryExpression):
            return self.evaluate_binary(expression)

        raise RuntimeMiniLangError(f"Unknown expression: {type(expression).__name__}")

    def evaluate_binary(self, expression):
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        operator = expression.operator

        if operator == "+":
            return self.trace_binary(expression, left + right)
        if operator == "-":
            return self.trace_binary(expression, left - right)
        if operator == "*":
            return self.trace_binary(expression, left * right)
        if operator == "/":
            if right == 0:
                raise RuntimeMiniLangError(
                    "Division by zero",
                    suggestion="Make sure the right side of '/' is not zero.",
                )
            return self.trace_binary(expression, left // right)
        if operator == "==":
            return self.trace_binary(expression, left == right)
        if operator == "!=":
            return self.trace_binary(expression, left != right)
        if operator == "<":
            return self.trace_binary(expression, left < right)
        if operator == ">":
            return self.trace_binary(expression, left > right)
        if operator == "<=":
            return self.trace_binary(expression, left <= right)
        if operator == ">=":
            return self.trace_binary(expression, left >= right)

        raise RuntimeMiniLangError(f"Unknown operator '{operator}'", suggestion="Use a supported MiniLang operator.")

    def trace_binary(self, expression, result):
        self.add_trace(f"Evaluated expression {expression.to_source()} = {self.format_value(result)}")
        return result

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise RuntimeMiniLangError(
            f"Variable '{name}' does not exist in memory",
            suggestion="Make sure the variable is declared before the program runs.",
        )

    def assign_variable(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise RuntimeMiniLangError(
            f"Variable '{name}' does not exist in memory",
            suggestion="Make sure the variable is declared before assignment.",
        )

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1]

    def memory_snapshot(self):
        return dict(self.scopes[0])

    def get_trace(self):
        return list(self.trace)

    def add_trace(self, message):
        if self.collect_trace:
            self.trace.append(message)

    def format_value(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)
