# VisuLang: A Visual Compiler for Learning Programming Languages

## Academic Project Report

**Course:** Compiler Design  
**Project Type:** Compiler / Interpreter with Visual Learning Dashboard  
**Language Implemented:** MiniLang  
**Implementation Language:** Python  
**GUI Framework:** PySide6  
**Prepared by:** ______________________________  
**Instructor:** ______________________________  
**Date:** ______________________________  

---

## Abstract

VisuLang is an educational compiler and interpreter project designed to demonstrate the main phases of compiler construction in a clear and beginner-friendly way. The project is built around a small programming language called MiniLang. MiniLang supports integer and boolean variables, declarations, assignments, arithmetic expressions, comparison expressions, print statements, if/else statements, while loops, and comments.

The main purpose of the project is not only to compile and execute a small language, but also to help students understand what happens inside a compiler. The system processes MiniLang source code through lexical analysis, syntax analysis, semantic analysis, intermediate code generation, code optimization, machine language generation, and final interpretation. A modern PySide6 graphical interface visualizes these phases using a pipeline, tables, trees, output panels, and step-by-step execution.

This report explains the design, implementation, compiler phases, visual interface, testing, limitations, and future improvements of VisuLang.

---

## 1. Introduction

Compiler Design is one of the most important subjects in computer science because it explains how programming languages are translated and executed. A compiler normally performs several phases, including lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, and target code generation.

Many students study these phases theoretically, but it can be difficult to understand how source code is transformed step by step. VisuLang solves this problem by turning a small compiler into a visual learning tool. The project allows a user to write MiniLang code, run the compiler, and observe the output of each phase separately.

The internal language is called MiniLang. The visual learning platform built around it is called VisuLang. The project therefore combines compiler theory with a practical, interactive software application.

---

## 2. Project Objectives

The main objectives of this project are:

1. To design a small programming language called MiniLang.
2. To implement a lexer that converts source code into tokens.
3. To implement a recursive descent parser that builds an Abstract Syntax Tree.
4. To implement semantic analysis using a symbol table.
5. To detect lexical, syntax, semantic, and runtime errors clearly.
6. To execute valid MiniLang programs using an interpreter.
7. To generate intermediate code after semantic analysis.
8. To optimize the intermediate code using simple optimization rules.
9. To generate educational machine language from optimized code.
10. To build a modern GUI that visualizes each compiler phase.
11. To provide a step-by-step mode for classroom demonstration.
12. To keep the project beginner-friendly and easy to present.

---

## 3. Problem Statement

Traditional compiler assignments often show only command-line output. Although this is useful, it does not always make the internal compiler pipeline easy to understand. Students may see that the compiler works, but they may not clearly see how the source code becomes tokens, how tokens become an AST, how semantic errors are detected, or how intermediate and machine code are produced.

The problem addressed by this project is the lack of visual explanation in simple compiler projects. VisuLang solves this by presenting each compiler phase in a separate visual section. It allows students to inspect the token table, AST tree, semantic symbol table, intermediate code, optimized code, machine language, execution trace, and final output.

---

## 4. Scope of the Project

The project is intentionally designed as an undergraduate-level compiler design project. It does not attempt to implement a full industrial compiler. Instead, it focuses on clarity and learning.

### Included in Scope

- MiniLang lexical analysis
- MiniLang recursive descent parsing
- Abstract Syntax Tree generation
- Semantic analysis with a symbol table
- Type checking for integers and booleans
- Interpreter execution
- Intermediate code generation
- Simple code optimization
- Toy machine language generation
- Command-line interface
- PySide6 graphical user interface
- Error reporting with suggestions
- Unit tests
- Example programs

### Not Included in Scope

- Real CPU machine code generation
- Register allocation
- Advanced optimization algorithms
- Functions and procedures
- Arrays or strings
- Object-oriented language features
- Full compiler backend for a real architecture

---

## 5. MiniLang Language Overview

MiniLang is a small educational programming language. It contains enough features to demonstrate important compiler concepts while remaining simple enough for students to understand.

### 5.1 Supported Data Types

MiniLang supports two basic data types:

| Type | Meaning | Example |
|---|---|---|
| `int` | Integer value | `int x = 5;` |
| `bool` | Boolean value | `bool flag = true;` |

### 5.2 Supported Statements

MiniLang supports the following statements:

| Statement Type | Example |
|---|---|
| Variable declaration | `int x = 5;` |
| Assignment | `x = x + 1;` |
| Print statement | `print(x);` |
| If statement | `if (x > 0) { print(x); }` |
| If/else statement | `if (flag) { print(1); } else { print(0); }` |
| While loop | `while (x < 10) { x = x + 1; }` |

### 5.3 Supported Operators

| Category | Operators |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Assignment | `=` |

### 5.4 Comments

MiniLang supports comments:

```minilang
// This is a single-line comment

/*
This is a multi-line comment
*/
```

---

## 6. MiniLang Grammar

The parser uses recursive descent parsing based on the following grammar:

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

This grammar gives correct operator precedence. Multiplication and division have higher precedence than addition and subtraction. Comparison and equality expressions are handled after arithmetic expressions.

---

## 7. System Architecture

VisuLang is divided into independent components. Each component handles one responsibility.

| File | Responsibility |
|---|---|
| `lexer.py` | Converts MiniLang source code into tokens |
| `parser.py` | Builds an Abstract Syntax Tree using recursive descent parsing |
| `ast_nodes.py` | Defines AST node classes |
| `semantic_analyzer.py` | Performs type checking and symbol table validation |
| `code_generator.py` | Generates intermediate code, optimized code, and machine language |
| `interpreter.py` | Executes the AST and collects execution trace |
| `errors.py` | Defines beginner-friendly error classes |
| `main.py` | Runs the compiler from the command line |
| `gui.py` | Provides the PySide6 visual learning dashboard |
| `examples/` | Contains valid and invalid MiniLang programs |
| `tests/` | Contains unit tests |

### 7.1 Compiler Pipeline

The complete pipeline is:

```text
Source Code
-> Lexical Analysis
-> Syntax Analysis
-> Semantic Analysis
-> Intermediate Code Generation
-> Code Optimization
-> Machine Language Generation
-> Interpretation
-> Program Output
```

The output section is intentionally placed last because it represents the final result after all compiler stages have completed successfully.

---

## 8. Lexical Analysis

Lexical analysis is the first compiler phase. It reads the raw source code character by character and groups characters into tokens. A token is a meaningful unit such as a keyword, identifier, integer literal, operator, or symbol.

### 8.1 Token Class

Each token contains:

- Token type
- Token value
- Line number
- Column number

Example:

```text
Token(INT, int)
Token(IDENTIFIER, x)
Token(ASSIGN, =)
Token(INTEGER, 5)
Token(SEMICOLON, ;)
```

The line and column values help the compiler show accurate error messages.

### 8.2 Recognized Tokens

The lexer recognizes:

| Category | Examples |
|---|---|
| Keywords | `int`, `bool`, `if`, `else`, `while`, `print`, `true`, `false` |
| Identifiers | `x`, `result`, `isLarge` |
| Integer literals | `5`, `10`, `100` |
| Operators | `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Symbols | `;`, `(`, `)`, `{`, `}` |
| Comments | `// comment`, `/* comment */` |
| EOF | End of file token |

### 8.3 Lexical Error Example

Source code:

```minilang
int x = 5 @ 2;
```

The character `@` is invalid in MiniLang. The lexer reports a lexical error and stops compilation.

Example message:

```text
Lexical Error:
Location: line 1, column 11
Message: Invalid character '@'
Suggestion: MiniLang supports letters, digits, keywords, operators, braces, parentheses, and semicolons.
```

---

## 9. Syntax Analysis

Syntax analysis is the second compiler phase. It checks whether the token sequence follows the grammar of the language. VisuLang uses a manually written recursive descent parser.

### 9.1 Recursive Descent Parsing

Recursive descent parsing is a top-down parsing technique. Each grammar rule is implemented as a method in the parser. For example:

- `statement()` parses statements.
- `declaration()` parses variable declarations.
- `assignment()` parses assignment statements.
- `expression()` parses expressions.
- `term()` and `factor()` handle arithmetic precedence.

This approach is suitable for MiniLang because the grammar is small and easy to understand.

### 9.2 Abstract Syntax Tree

The parser builds an Abstract Syntax Tree, also called an AST. The AST is a tree representation of the program structure. It removes unnecessary syntax details and keeps the meaningful structure of the program.

Example source code:

```minilang
int x = 5;
print(x);
```

AST:

```text
Program
  Declaration
    Type: int
    Name: x
    Value:
      Integer: 5
  Print
    Expression:
      Identifier: x
```

### 9.3 Syntax Error Example

Source code:

```minilang
int x = 5
print(x);
```

The declaration is missing a semicolon. The parser reports a syntax error.

Example message:

```text
Syntax Error:
Message: Missing semicolon after declaration.
Suggestion: Add ';' at the end of the declaration.
```

---

## 10. Semantic Analysis

Semantic analysis checks the meaning of the program after the syntax is valid. A program can have correct syntax but still be semantically wrong.

Example:

```minilang
int age = 20;
age = true;
```

This is syntactically valid, but semantically incorrect because a boolean value cannot be assigned to an integer variable.

### 10.1 Symbol Table

The semantic analyzer uses a symbol table to store declared variables and their types.

Example symbol table:

| Variable | Type |
|---|---|
| `x` | `int` |
| `result` | `int` |
| `isLarge` | `bool` |

### 10.2 Semantic Checks

The semantic analyzer checks:

1. Variables must be declared before use.
2. Variables cannot be declared twice in the same scope.
3. Assignment values must match variable types.
4. Arithmetic operators must use integer operands.
5. Comparison operators return boolean values.
6. If conditions must be boolean.
7. While conditions must be boolean.
8. Print statements can print integer or boolean values.

### 10.3 Semantic Error Example

Source code:

```minilang
print(x);
```

The variable `x` was never declared.

Example message:

```text
Semantic Error:
Message: Variable 'x' used before declaration
Suggestion: Declare it first, for example: int x;
```

---

## 11. Intermediate Code Generation

Intermediate code generation is an additional compiler phase added to make the project closer to a full compiler. It converts the AST into a simpler representation that is easier to optimize and translate.

VisuLang generates three-address code. Three-address code breaks expressions into small instructions using temporary variables.

### 11.1 Example Source Code

```minilang
int x;
int y;

x = 10 * 2;
y = x;
y = y;

print(y);
```

### 11.2 Normal Intermediate Code

```text
01: DECLARE int x
02: DECLARE int y
03: t1 = 10 * 2
04: x = t1
05: y = x
06: y = y
07: PRINT y
```

The expression `10 * 2` is stored in temporary variable `t1`. The instruction `y = y` is valid but useless.

---

## 12. Code Optimization

Optimization improves intermediate code without changing the final meaning of the program. VisuLang includes simple optimizations that are easy to explain in class.

### 12.1 Optimizations Used

| Optimization | Meaning | Example |
|---|---|---|
| Constant folding | Evaluate constant expressions at compile time | `10 * 2` becomes `20` |
| Remove self-assignment | Remove assignments that do nothing | `y = y` is removed |
| Remove jump to next label | Remove unnecessary jumps | `GOTO L1` followed by `LABEL L1` |

### 12.2 Optimized Intermediate Code

Before optimization:

```text
03: t1 = 10 * 2
06: y = y
```

After optimization:

```text
03: t1 = 20
```

Full optimized code:

```text
01: DECLARE int x
02: DECLARE int y
03: t1 = 20
04: x = t1
05: y = x
06: PRINT y
```

The optimized code is shorter and simpler, but the program output remains the same.

---

## 13. Machine Language Generation

After optimization, VisuLang translates the optimized intermediate code into a simple educational machine language. This is not real binary CPU code. It is an assembly-style representation designed to demonstrate the idea of target code generation.

### 13.1 Example Machine Language

Optimized intermediate code:

```text
t1 = 20
x = t1
y = x
PRINT y
```

Machine language:

```text
01: LOAD 20
02: STORE t1
03: LOAD t1
04: STORE x
05: LOAD x
06: STORE y
07: PRINT y
```

### 13.2 Machine Instructions

| Instruction | Meaning |
|---|---|
| `ALLOC x` | Reserve memory for variable `x` |
| `LOAD value` | Load a value into the accumulator |
| `STORE x` | Store accumulator value into variable `x` |
| `ADD value` | Add a value |
| `SUB value` | Subtract a value |
| `MUL value` | Multiply by a value |
| `DIV value` | Divide by a value |
| `CMP_GT value` | Compare greater-than |
| `CMP_LT value` | Compare less-than |
| `JMP label` | Jump to a label |
| `JZ label` | Jump if value is false or zero |
| `PRINT value` | Print a value |

This stage helps demonstrate how compilers can translate higher-level code into lower-level instructions.

---

## 14. Interpretation and Execution

After the compiler phases complete successfully, the interpreter executes the AST. The interpreter stores variables in memory, evaluates expressions, executes conditions and loops, and collects print output.

### 14.1 Interpreter Responsibilities

- Store variable values.
- Execute declarations.
- Execute assignments.
- Evaluate arithmetic and comparison expressions.
- Execute print statements.
- Execute if/else statements.
- Execute while loops.
- Stop infinite loops using a maximum loop iteration limit.

### 14.2 Execution Trace

The interpreter can collect trace messages for the GUI. These messages explain what happens during execution.

Example trace:

```text
1. Declared variable x = 5
2. Declared variable y = 10
3. Evaluated expression y * 2 = 20
4. Evaluated expression x + y * 2 = 25
5. Assigned result = 25
6. Printed 25
```

The execution trace is useful for students because it explains the runtime behavior of the program step by step.

---

## 15. Graphical User Interface

VisuLang includes a modern graphical user interface built using PySide6. The GUI transforms the compiler into an interactive learning dashboard.

### 15.1 GUI Main Features

- Source code editor
- Run Compiler button
- Run Step by Step button
- Reset Steps button
- Clear button
- Load Example button
- Save Code button
- Compiler pipeline visualization
- Token table
- AST tree view
- Semantic symbol table
- Intermediate code tab
- Optimized code tab
- Machine language tab
- Execution trace tab
- Errors tab
- Final program output tab

### 15.2 Visual Pipeline

The GUI displays the compiler pipeline:

```text
Source -> Lexer -> Parser -> Semantic -> IR -> Optimize -> Machine -> Interpreter -> Output
```

Each stage can have one of four states:

| State | Meaning |
|---|---|
| Waiting | The stage has not started |
| Active | The stage is currently running |
| Passed | The stage completed successfully |
| Failed | The stage produced an error |

### 15.3 Step-by-Step Mode

Step-by-step mode is one of the most important learning features. Each click runs one compiler phase:

| Click | Result |
|---|---|
| 1 | Lexical analysis and token table |
| 2 | Syntax analysis and AST tree |
| 3 | Semantic analysis and symbol table |
| 4 | Intermediate code generation |
| 5 | Code optimization |
| 6 | Machine language generation |
| 7 | Interpretation, execution trace, and final output |

This allows a presenter to pause after each phase and explain what changed.

---

## 16. Error Handling

Error handling is designed to be beginner-friendly. Errors are not only reported, but also explained using suggestions.

### 16.1 Error Types

| Error Type | Example Cause |
|---|---|
| Lexical Error | Invalid character |
| Syntax Error | Missing semicolon or brace |
| Semantic Error | Undeclared variable or type mismatch |
| Runtime Error | Division by zero or possible infinite loop |

### 16.2 Error Message Format

Example:

```text
Syntax Error:
Location: line 2, column 1
Message: Missing semicolon after declaration.
Suggestion: Add ';' at the end of the declaration.
```

The GUI also marks the failed compiler stage in red.

---

## 17. Example Program

The following program demonstrates declarations, assignments, arithmetic, comparison, if/else, while loop, and print statements.

```minilang
int x = 5;
int y = 10;
int result;
bool isLarge;

result = x + y * 2;
isLarge = result > 20;

if (isLarge) {
    print(result);
} else {
    print(0);
}

while (x < 10) {
    x = x + 1;
    print(x);
}
```

### 17.1 Program Output

```text
25
6
7
8
9
10
```

### 17.2 Explanation

The expression `y * 2` is evaluated first because multiplication has higher precedence than addition. Since `y` is 10, `y * 2` becomes 20. Then `x + 20` becomes 25. The variable `isLarge` becomes true because `result > 20`. Therefore, the if statement prints 25. The while loop then increments `x` from 5 to 10 and prints each new value.

---

## 18. Testing

The project includes unit tests in `tests/test_minilang.py`. These tests verify that important compiler features work correctly.

### 18.1 Test Cases

| Test | Purpose |
|---|---|
| Lexer token generation | Checks that source code becomes the expected tokens |
| Parser AST generation | Checks that parser creates correct AST nodes |
| Undeclared variable detection | Checks semantic error handling |
| Wrong assignment type detection | Checks type compatibility |
| Interpreter output | Checks that valid programs execute correctly |
| Execution trace | Checks that trace messages are collected |
| Code generation | Checks intermediate, optimized, and machine code generation |

### 18.2 Test Command

```bash
python -m unittest discover -s tests
```

Expected result:

```text
Ran 7 tests
OK
```

---

## 19. How to Run the Project

### 19.1 Run the Command-Line Version

From inside the `MiniLangCompiler` folder:

```bash
python main.py examples/valid_program.minilang
```

This displays:

1. Source code
2. Lexical analysis output
3. Syntax analysis output
4. Semantic analysis output
5. Intermediate code
6. Optimized code
7. Machine language
8. Final program output

### 19.2 Run the GUI

Install PySide6:

```bash
pip install PySide6
```

Run the GUI:

```bash
python gui.py
```

The GUI allows the user to type MiniLang code, run the compiler, inspect each phase, and use step-by-step mode.

---

## 20. Demonstration Plan

A suggested presentation demonstration is:

1. Open the command-line version and run `valid_program.minilang`.
2. Explain the output sections one by one.
3. Open the VisuLang GUI.
4. Show the source code editor.
5. Click Run Compiler and show the full visual pipeline.
6. Open the Tokens tab and explain lexical analysis.
7. Open the AST tab and explain syntax analysis.
8. Open the Semantic Analysis tab and explain the symbol table.
9. Open the Intermediate Code tab and explain three-address code.
10. Open the Optimized Code tab and explain constant folding.
11. Open the Machine Language tab and explain target code generation.
12. Open the Program Output tab and show the final result.
13. Use Run Step by Step to demonstrate each phase slowly.
14. Load an invalid example and show beginner-friendly error messages.

---

## 21. Limitations

Although VisuLang demonstrates many compiler concepts, it has some limitations:

1. The language supports only integers and booleans.
2. There are no functions or procedures.
3. There are no arrays, strings, or user-defined types.
4. The machine language is educational and not real CPU binary code.
5. Optimization is simple and does not include advanced data-flow analysis.
6. The interpreter executes the AST directly instead of executing machine code.
7. The GUI requires PySide6 installation.

These limitations are acceptable because the project is designed for learning, not production use.

---

## 22. Future Improvements

Possible future improvements include:

1. Add string variables.
2. Add functions and return values.
3. Add arrays.
4. Add nested function scopes.
5. Add more optimization techniques.
6. Execute the generated machine language using a virtual machine.
7. Add syntax highlighting to the source editor.
8. Add export buttons for tokens, AST, and generated code.
9. Add a visual flowchart for if/else and while loops.
10. Add more detailed runtime memory visualization.

---

## 23. Conclusion

VisuLang successfully transforms a simple compiler assignment into a visual learning compiler. It demonstrates the essential phases of compiler design, including lexical analysis, syntax analysis, semantic analysis, intermediate code generation, code optimization, machine language generation, and final interpretation.

The project remains beginner-friendly because the language is small, the code is organized into clear modules, and the GUI presents each phase visually. The step-by-step mode, token table, AST tree, symbol table, intermediate code, optimized code, machine language, execution trace, and error display make the project suitable for classroom presentation.

Overall, VisuLang shows how compiler theory can be connected to a working software system that students can run, inspect, and understand.

---

## References

1. Aho, A. V., Lam, M. S., Sethi, R., and Ullman, J. D. *Compilers: Principles, Techniques, and Tools*. Pearson.
2. Louden, K. C. *Compiler Construction: Principles and Practice*. Cengage Learning.
3. Python Software Foundation. *Python Documentation*.
4. Qt Group. *PySide6 Documentation*.

---

## Appendix A: Project Folder Structure

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
|-- academic_report.md
|-- presentation/
|   |-- presentation_outline.md
```

---

## Appendix B: Screenshot Placeholders

Add screenshots in the final submitted version:

```text
[Screenshot 1: VisuLang main dashboard]
[Screenshot 2: Compiler pipeline after successful run]
[Screenshot 3: Token table]
[Screenshot 4: AST tree]
[Screenshot 5: Semantic symbol table]
[Screenshot 6: Intermediate code tab]
[Screenshot 7: Optimized code tab]
[Screenshot 8: Machine language tab]
[Screenshot 9: Execution trace]
[Screenshot 10: Error handling example]
```
