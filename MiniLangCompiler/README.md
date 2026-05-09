# VisuLang: A Visual Compiler for Learning Programming Languages

## Group Members

- Student 1: ____________________
- Student 2: ____________________
- Student 3: ____________________

## Project Description

VisuLang is an educational visual compiler built around a small programming language called MiniLang. The compiler internals stay simple and beginner-friendly, while the GUI turns the compiler pipeline into a modern learning dashboard.

The compiler flow is:

```text
Source Code -> Lexical Analysis -> Syntax Analysis -> Semantic Analysis
-> Intermediate Code -> Optimization -> Machine Language -> Execution -> Output
```

## Why This Project Is Special

VisuLang is more than a normal compiler assignment. It helps students see what happens inside each compiler phase.

Main visual features:

- Modern PySide6 dark dashboard
- Animated compiler pipeline
- Step-by-step mode
- Token table with line and column numbers
- AST tree visualization
- Semantic symbol table
- Intermediate code generation
- Optimized code display
- Machine language display
- Program output view
- Execution trace
- Beginner-friendly error messages with suggestions

## Project Structure

```text
MiniLangCompiler/
|-- main.py
|-- gui.py
|-- lexer.py
|-- parser.py
|-- ast_nodes.py
|-- semantic_analyzer.py
|-- code_generator.py
|-- interpreter.py
|-- errors.py
|-- examples/
|   |-- valid_program.minilang
|   |-- lexical_error.minilang
|   |-- syntax_error.minilang
|   |-- semantic_error.minilang
|-- tests/
|   |-- test_minilang.py
|-- README.md
|-- presentation/
|   |-- presentation_outline.md
```

## MiniLang Language Features

MiniLang supports:

- Integer variables
- Boolean variables
- Variable declarations
- Assignment statements
- Arithmetic expressions: `+`, `-`, `*`, `/`
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- `if` and `else` statements
- `while` loops
- `print` statements
- Single-line comments using `//`
- Multi-line comments using `/* ... */`
- Lexical, syntax, semantic, and runtime errors

## PySide6 Visual Dashboard

The new GUI is built with PySide6 and uses:

- `QApplication`
- `QMainWindow`
- `QSplitter`
- `QTabWidget`
- `QPlainTextEdit`
- `QTableWidget`
- `QTreeWidget`
- `QFrame`
- `QPropertyAnimation`
- `QGraphicsOpacityEffect`
- `QTimer`

The layout is designed as a professional educational dashboard:

- Left side: source code editor and action buttons
- Right side: visualization tabs
- Top: VisuLang title and animated compiler pipeline
- Dark theme with rounded cards and modern colors

## Visual Compiler Pipeline

The GUI shows this pipeline:

```text
Source -> Lexer -> Parser -> Semantic -> IR -> Optimize -> Machine -> Interpreter -> Output
```

Each stage has one of these states:

- Waiting
- Active
- Passed
- Failed

When a phase runs, the matching pipeline card becomes active. When it succeeds, it turns green. If an error happens, the failed stage turns red and the Errors tab is shown.

## Step-by-Step Mode

The `Run Step by Step` button runs one compiler phase per click:

1. First click: lexical analysis and token table
2. Second click: syntax analysis and AST tree
3. Third click: semantic analysis and symbol table
4. Fourth click: intermediate code generation
5. Fifth click: code optimization
6. Sixth click: machine language generation
7. Seventh click: interpretation, execution trace, and final program output

The `Reset Steps` button clears the current step state and returns the pipeline to waiting mode.

## Token Table

The Tokens tab displays tokens in a table:

```text
Index | Token Type | Value | Line | Column
0     | INT        | int   | 1    | 1
1     | IDENTIFIER | x     | 1    | 5
2     | ASSIGN     | =     | 1    | 7
3     | INTEGER    | 5     | 1    | 9
```

This makes lexical analysis easier to inspect than a plain text list.

## AST Tree Visualization

The AST tab uses a `QTreeWidget` to show the syntax tree as expandable nodes.

Example:

```text
Program
  Declaration
    Type: int
    Name: x
    Value:
      Integer: 5
```

A fallback plain-text AST view is also shown below the tree.

## Intermediate Code

After semantic analysis passes, VisuLang generates three-address intermediate code. This is inspired by common compiler lab exercises where expressions are broken into simple temporary-variable instructions.

Example:

```text
01: DECLARE int x
02: x = 5
03: t1 = y * 2
04: t2 = x + t1
05: result = t2
```

## Code Optimization

The Optimized Code tab applies beginner-friendly optimizations, such as:

- Constant folding, for example `t1 = 10 * 2` becomes `t1 = 20`
- Removing useless self-assignments such as `x = x`
- Removing jumps that go directly to the next label

The goal is to show the idea of optimization clearly without making the project too advanced.

## Machine Language

The Machine Language tab translates optimized intermediate code into a small educational assembly-style language.

Example:

```text
01: LOAD y
02: MUL 2
03: STORE t1
04: LOAD t1
05: STORE result
06: PRINT result
```

This is a toy machine language for classroom demonstration, not real CPU binary code.

## Semantic Symbol Table

The Semantic Analysis tab shows:

- Passed or failed status
- Variable name
- Variable type
- Current value after execution, when available

Example:

```text
x        int     10
result   int     25
isLarge  bool    true
```

## Execution Trace

The Execution Trace tab shows what the interpreter does step by step.

Example:

```text
Declared variable x = 5
Declared variable y = 10
Evaluated expression y * 2 = 20
Assigned result = 25
Condition result > 20 evaluated to true
Printed 25
```

Trace collection is optional and does not change normal command-line output.

## Beginner-Friendly Errors

The Errors tab shows:

- Error type
- Message
- Line and column, when available
- Suggestion

Example:

```text
Syntax Error:
Location: line 2, column 1
Message: Missing semicolon after declaration.
Suggestion: Add ';' at the end of the declaration.
```

The failed compiler phase is also marked red in the pipeline.

## Grammar

```text
program        -> statement*
statement      -> declaration | assignment | print_stmt | if_stmt | while_stmt
declaration    -> type IDENTIFIER ("=" expression)? ";"
type           -> "int" | "bool"
assignment     -> IDENTIFIER "=" expression ";"
print_stmt     -> "print" "(" expression ")" ";"
if_stmt        -> "if" "(" expression ")" block ("else" block)?
while_stmt     -> "while" "(" expression ")" block
block          -> "{" statement* "}"
expression     -> equality
equality       -> comparison (("==" | "!=") comparison)*
comparison     -> term (("<" | ">" | "<=" | ">=") term)*
term           -> factor (("+" | "-") factor)*
factor         -> unary (("*" | "/") unary)*
unary          -> "-" unary | primary
primary        -> INTEGER | "true" | "false" | IDENTIFIER | "(" expression ")"
```

## Install GUI Dependency

The command-line compiler uses pure Python. The GUI requires PySide6.

```bash
pip install PySide6
```

## Run the GUI

From inside the `MiniLangCompiler` folder:

```bash
python gui.py
```

## Run the Command-Line Version

From inside the `MiniLangCompiler` folder:

```bash
python main.py examples/valid_program.minilang
```

Try the error examples:

```bash
python main.py examples/lexical_error.minilang
python main.py examples/syntax_error.minilang
python main.py examples/semantic_error.minilang
```

## Run Tests

```bash
python -m unittest discover -s tests
```

The tests check:

- Lexer token generation
- Parser AST generation
- Semantic analyzer errors
- Intermediate code, optimized code, and machine language generation
- Interpreter output
- Optional execution trace collection

## Screenshots

Add screenshots here:

```text
[Insert screenshot of the PySide6 dashboard]
[Insert screenshot of the animated pipeline]
[Insert screenshot of the token table]
[Insert screenshot of the AST tree]
[Insert screenshot of the intermediate code tab]
[Insert screenshot of the optimized code tab]
[Insert screenshot of the machine language tab]
[Insert screenshot of the execution trace]
```

## Conclusion

VisuLang keeps the MiniLang compiler simple internally, but presents it as a polished visual learning tool. It clearly demonstrates lexical analysis, syntax analysis, semantic analysis, intermediate code, optimization, machine language, and final interpretation output in a way students can explore step by step.
