"""AST node classes for MiniLang.

The parser builds these nodes. The semantic analyzer checks them, and the
interpreter executes them.
"""

from dataclasses import dataclass


def indent(level):
    return "  " * level


def format_literal(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class ASTNode:
    def pretty(self, level=0):
        raise NotImplementedError


class Expression(ASTNode):
    def to_source(self):
        raise NotImplementedError


@dataclass
class Program(ASTNode):
    statements: list

    def pretty(self, level=0):
        lines = [f"{indent(level)}Program"]
        for statement in self.statements:
            lines.extend(statement.pretty(level + 1))
        return lines

    def __str__(self):
        return "\n".join(self.pretty())


@dataclass
class Block(ASTNode):
    statements: list

    def pretty(self, level=0):
        lines = [f"{indent(level)}Block"]
        for statement in self.statements:
            lines.extend(statement.pretty(level + 1))
        return lines


@dataclass
class Declaration(ASTNode):
    var_type: str
    name: str
    initializer: Expression = None

    def pretty(self, level=0):
        lines = [
            f"{indent(level)}Declaration",
            f"{indent(level + 1)}Type: {self.var_type}",
            f"{indent(level + 1)}Name: {self.name}",
        ]
        if self.initializer is not None:
            lines.append(f"{indent(level + 1)}Value:")
            lines.extend(self.initializer.pretty(level + 2))
        else:
            lines.append(f"{indent(level + 1)}Value: <default>")
        return lines


@dataclass
class Assignment(ASTNode):
    name: str
    expression: Expression

    def pretty(self, level=0):
        lines = [f"{indent(level)}Assignment", f"{indent(level + 1)}Name: {self.name}"]
        lines.append(f"{indent(level + 1)}Value:")
        lines.extend(self.expression.pretty(level + 2))
        return lines


@dataclass
class PrintStatement(ASTNode):
    expression: Expression

    def pretty(self, level=0):
        lines = [f"{indent(level)}Print"]
        lines.append(f"{indent(level + 1)}Expression:")
        lines.extend(self.expression.pretty(level + 2))
        return lines


@dataclass
class IfStatement(ASTNode):
    condition: Expression
    then_block: Block
    else_block: Block = None

    def pretty(self, level=0):
        lines = [f"{indent(level)}If Statement"]
        lines.append(f"{indent(level + 1)}Condition:")
        lines.extend(self.condition.pretty(level + 2))
        lines.append(f"{indent(level + 1)}Then:")
        lines.extend(self.then_block.pretty(level + 2))
        if self.else_block is not None:
            lines.append(f"{indent(level + 1)}Else:")
            lines.extend(self.else_block.pretty(level + 2))
        return lines


@dataclass
class WhileStatement(ASTNode):
    condition: Expression
    body: Block

    def pretty(self, level=0):
        lines = [f"{indent(level)}While Statement"]
        lines.append(f"{indent(level + 1)}Condition:")
        lines.extend(self.condition.pretty(level + 2))
        lines.append(f"{indent(level + 1)}Body:")
        lines.extend(self.body.pretty(level + 2))
        return lines


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def pretty(self, level=0):
        lines = [f"{indent(level)}BinaryExpression: {self.operator}"]
        lines.append(f"{indent(level + 1)}Left:")
        lines.extend(self.left.pretty(level + 2))
        lines.append(f"{indent(level + 1)}Right:")
        lines.extend(self.right.pretty(level + 2))
        return lines

    def to_source(self):
        return f"{self.left.to_source()} {self.operator} {self.right.to_source()}"


@dataclass
class UnaryExpression(Expression):
    operator: str
    expression: Expression

    def pretty(self, level=0):
        lines = [f"{indent(level)}UnaryExpression: {self.operator}"]
        lines.append(f"{indent(level + 1)}Expression:")
        lines.extend(self.expression.pretty(level + 2))
        return lines

    def to_source(self):
        return f"{self.operator}{self.expression.to_source()}"


@dataclass
class Literal(Expression):
    value: object
    value_type: str

    def pretty(self, level=0):
        label = "Integer" if self.value_type == "int" else "Boolean"
        return [f"{indent(level)}{label}: {format_literal(self.value)}"]

    def to_source(self):
        return format_literal(self.value)


@dataclass
class Identifier(Expression):
    name: str

    def pretty(self, level=0):
        return [f"{indent(level)}Identifier: {self.name}"]

    def to_source(self):
        return self.name
