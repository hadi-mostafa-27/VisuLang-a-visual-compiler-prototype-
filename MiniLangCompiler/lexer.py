"""Lexical analyzer for MiniLang.

The lexer reads raw source code and converts it into a list of tokens.
Each token contains a type, its original value, and its source position.
"""

from dataclasses import dataclass

from errors import LexicalError


@dataclass
class Token:
    token_type: str
    value: object
    line: int
    column: int

    def __str__(self):
        return f"Token({self.token_type}, {self.value})"

    def __repr__(self):
        return str(self)


class Lexer:
    KEYWORDS = {
        "int": "INT",
        "bool": "BOOL",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "print": "PRINT",
        "true": "TRUE",
        "false": "FALSE",
    }

    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_column = 1

    def scan_tokens(self):
        """Convert the whole source program into tokens."""
        while not self.is_at_end():
            self.start = self.current
            self.start_column = self.column
            self.scan_token()

        self.tokens.append(Token("EOF", "EOF", self.line, self.column))
        return self.tokens

    # A friendly alias for students who expect the word "tokenize".
    def tokenize(self):
        return self.scan_tokens()

    def scan_token(self):
        char = self.advance()

        if char in " \r\t":
            return
        if char == "\n":
            return
        if char == "+":
            self.add_token("PLUS", char)
        elif char == "-":
            self.add_token("MINUS", char)
        elif char == "*":
            self.add_token("STAR", char)
        elif char == "/":
            self.handle_slash()
        elif char == "=":
            self.add_token("EQUAL" if self.match("=") else "ASSIGN", "==" if self.previous_two_chars_are("==") else "=")
        elif char == "!":
            if self.match("="):
                self.add_token("NOT_EQUAL", "!=")
            else:
                raise LexicalError(
                    "Unexpected character '!'. MiniLang only supports '!=' for not-equal.",
                    self.line,
                    self.start_column,
                    "Use '!=' for comparison, or remove '!'.",
                )
        elif char == "<":
            self.add_token("LESS_EQUAL" if self.match("=") else "LESS", "<=" if self.previous_two_chars_are("<=") else "<")
        elif char == ">":
            self.add_token("GREATER_EQUAL" if self.match("=") else "GREATER", ">=" if self.previous_two_chars_are(">=") else ">")
        elif char == ";":
            self.add_token("SEMICOLON", char)
        elif char == "(":
            self.add_token("LPAREN", char)
        elif char == ")":
            self.add_token("RPAREN", char)
        elif char == "{":
            self.add_token("LBRACE", char)
        elif char == "}":
            self.add_token("RBRACE", char)
        elif char.isdigit():
            self.integer()
        elif char.isalpha() or char == "_":
            self.identifier()
        else:
            raise LexicalError(
                f"Invalid character '{char}'",
                self.line,
                self.start_column,
                "MiniLang supports letters, digits, keywords, operators, braces, parentheses, and semicolons.",
            )

    def handle_slash(self):
        if self.match("/"):
            # Single-line comment: ignore everything until the next line.
            while not self.is_at_end() and self.peek() != "\n":
                self.advance()
        elif self.match("*"):
            # Multi-line comment: ignore everything until the closing */.
            self.block_comment()
        else:
            self.add_token("SLASH", "/")

    def block_comment(self):
        while not self.is_at_end():
            if self.peek() == "*" and self.peek_next() == "/":
                self.advance()
                self.advance()
                return
            self.advance()

        raise LexicalError(
            "Unterminated block comment",
            self.line,
            self.column,
            "Close the comment with */.",
        )

    def integer(self):
        while self.peek().isdigit():
            self.advance()

        text = self.source_code[self.start:self.current]
        self.add_token("INTEGER", int(text))

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source_code[self.start:self.current]
        token_type = self.KEYWORDS.get(text, "IDENTIFIER")
        self.add_token(token_type, text)

    def add_token(self, token_type, value):
        self.tokens.append(Token(token_type, value, self.line, self.start_column))

    def advance(self):
        char = self.source_code[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source_code[self.current] != expected:
            return False
        self.advance()
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source_code[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source_code):
            return "\0"
        return self.source_code[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source_code)

    def previous_two_chars_are(self, text):
        return self.source_code[self.current - 2:self.current] == text
