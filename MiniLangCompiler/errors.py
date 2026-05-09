"""Custom error classes for the MiniLang/VisuLang project."""


class MiniLangError(Exception):
    """Base class for all MiniLang errors.

    The GUI uses ``to_display`` to show beginner-friendly error messages.
    ``__str__`` also uses the same format so command-line mode benefits too.
    """

    label = "MiniLang Error"

    def __init__(self, message, line=None, column=None, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        super().__init__(self.message)

    def __str__(self):
        return self.to_display()

    def to_display(self):
        lines = [f"{self.label}:"]
        if self.line is not None and self.column is not None:
            lines.append(f"Location: line {self.line}, column {self.column}")
        lines.append(f"Message: {self.message}")
        if self.suggestion:
            lines.append(f"Suggestion: {self.suggestion}")
        return "\n".join(lines)


class LexicalError(MiniLangError):
    """Raised when the lexer finds an invalid character or token."""

    label = "Lexical Error"

    def __init__(self, message, line=None, column=None, suggestion=None):
        if suggestion is None:
            suggestion = "Remove the invalid character or replace it with a valid MiniLang symbol."
        super().__init__(message, line, column, suggestion)


class ParserError(MiniLangError):
    """Raised when the parser finds invalid MiniLang syntax."""

    label = "Syntax Error"

    def __init__(self, message, line=None, column=None, suggestion=None):
        super().__init__(message, line, column, suggestion)


class SemanticError(MiniLangError):
    """Raised when semantic rules are broken."""

    label = "Semantic Error"

    def __init__(self, message, line=None, column=None, suggestion=None):
        super().__init__(message, line, column, suggestion)


class RuntimeMiniLangError(MiniLangError):
    """Raised when the interpreter fails while running a valid AST."""

    label = "Runtime Error"

    def __init__(self, message, line=None, column=None, suggestion=None):
        if suggestion is None:
            suggestion = "Check the values used during execution, especially loop conditions and division."
        super().__init__(message, line, column, suggestion)
