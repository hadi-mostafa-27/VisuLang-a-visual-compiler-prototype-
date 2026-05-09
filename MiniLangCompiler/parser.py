"""Recursive descent parser for MiniLang."""

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
from errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.check("EOF"):
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self.match("INT", "BOOL"):
            return self.declaration()
        if self.match("IDENTIFIER"):
            return self.assignment(self.previous())
        if self.match("PRINT"):
            return self.print_statement()
        if self.match("IF"):
            return self.if_statement()
        if self.match("WHILE"):
            return self.while_statement()

        token = self.peek()
        raise ParserError(
            f"Expected a statement but found '{token.value}'",
            token.line,
            token.column,
            "Start a statement with int, bool, an identifier, print, if, or while.",
        )

    def declaration(self):
        type_token = self.previous()
        name_token = self.consume(
            "IDENTIFIER",
            "Missing variable name after type.",
            "Write declarations like: int x; or bool isReady;",
        )

        initializer = None
        if self.match("ASSIGN"):
            initializer = self.expression()

        self.consume(
            "SEMICOLON",
            "Missing semicolon after declaration.",
            "Add ';' at the end of the declaration.",
        )
        return Declaration(type_token.value, name_token.value, initializer)

    def assignment(self, name_token):
        self.consume("ASSIGN", "Missing '=' after variable name.", "Write assignments like: x = 5;")
        value = self.expression()
        self.consume("SEMICOLON", "Missing semicolon after assignment.", "Add ';' at the end of the assignment.")
        return Assignment(name_token.value, value)

    def print_statement(self):
        self.consume("LPAREN", "Missing '(' after print.", "Write print statements like: print(x);")
        value = self.expression()
        self.consume("RPAREN", "Missing ')' after print expression.", "Close the print expression with ')'.")
        self.consume("SEMICOLON", "Missing semicolon after print statement.", "Add ';' after print(...).")
        return PrintStatement(value)

    def if_statement(self):
        self.consume("LPAREN", "Missing '(' after if.", "Write if conditions like: if (x > 0) { ... }")
        condition = self.expression()
        self.consume("RPAREN", "Missing ')' after if condition.", "Close the condition before the block.")
        then_block = self.block()

        else_block = None
        if self.match("ELSE"):
            else_block = self.block()

        return IfStatement(condition, then_block, else_block)

    def while_statement(self):
        self.consume("LPAREN", "Missing '(' after while.", "Write while loops like: while (x < 10) { ... }")
        condition = self.expression()
        self.consume("RPAREN", "Missing ')' after while condition.", "Close the condition before the block.")
        body = self.block()
        return WhileStatement(condition, body)

    def block(self):
        self.consume("LBRACE", "Missing '{' to start block.", "Start the block with '{'.")
        statements = []

        while not self.check("RBRACE") and not self.check("EOF"):
            statements.append(self.statement())

        self.consume("RBRACE", "Missing '}' after block.", "Add '}' to close the block.")
        return Block(statements)

    # expression -> equality
    def expression(self):
        return self.equality()

    # equality -> comparison (("==" | "!=") comparison)*
    def equality(self):
        expression = self.comparison()

        while self.match("EQUAL", "NOT_EQUAL"):
            operator = self.previous().value
            right = self.comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    # comparison -> term (("<" | ">" | "<=" | ">=") term)*
    def comparison(self):
        expression = self.term()

        while self.match("LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"):
            operator = self.previous().value
            right = self.term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    # term -> factor (("+" | "-") factor)*
    def term(self):
        expression = self.factor()

        while self.match("PLUS", "MINUS"):
            operator = self.previous().value
            right = self.factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    # factor -> unary (("*" | "/") unary)*
    def factor(self):
        expression = self.unary()

        while self.match("STAR", "SLASH"):
            operator = self.previous().value
            right = self.unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    # unary -> "-" unary | primary
    def unary(self):
        if self.match("MINUS"):
            operator = self.previous().value
            right = self.unary()
            return UnaryExpression(operator, right)

        return self.primary()

    # primary -> INTEGER | "true" | "false" | IDENTIFIER | "(" expression ")"
    def primary(self):
        if self.match("INTEGER"):
            return Literal(self.previous().value, "int")
        if self.match("TRUE"):
            return Literal(True, "bool")
        if self.match("FALSE"):
            return Literal(False, "bool")
        if self.match("IDENTIFIER"):
            return Identifier(self.previous().value)
        if self.match("LPAREN"):
            expression = self.expression()
            self.consume("RPAREN", "Missing ')' after expression.", "Close the expression with ')'.")
            return expression

        token = self.peek()
        raise ParserError(
            f"Expected expression but found '{token.value}'",
            token.line,
            token.column,
            "Use an integer, true, false, variable name, or parenthesized expression.",
        )

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type, message, suggestion=None):
        if self.check(token_type):
            return self.advance()

        token = self.peek()
        raise ParserError(message, token.line, token.column, suggestion)

    def check(self, token_type):
        if self.is_at_end():
            return token_type == "EOF"
        return self.peek().token_type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
