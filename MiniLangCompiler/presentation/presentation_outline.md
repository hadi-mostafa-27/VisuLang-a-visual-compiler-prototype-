# VisuLang Presentation Outline

## Slide 1: Title

**VisuLang: A Visual Compiler for Learning Programming Languages**

Speaker Notes:

- Introduce VisuLang as Part 2 of the MiniLang compiler project.
- Explain that MiniLang is still the internal language, but VisuLang is the visual learning tool built around it.

## Slide 2: Project Objective

Content:

- Upgrade a normal compiler assignment into an educational tool
- Show each compiler phase visually
- Help students understand how source code becomes output
- Present the compiler in a modern PySide6 dashboard

Speaker Notes:

- Emphasize that the goal is learning and visualization, not building a large production compiler.

## Slide 3: What is MiniLang?

Content:

- Small programming language used by VisuLang
- Supports `int`, `bool`, declarations, assignment, `if`, `while`, and `print`
- Simple enough to explain in class

Speaker Notes:

- Mention that MiniLang gives the compiler enough features to demonstrate real compiler behavior.

## Slide 4: Visual Compiler Pipeline

Content:

```text
Source -> Tokens -> AST -> Semantic Check -> Intermediate Code -> Optimized Code -> Machine Language -> Output
```

Speaker Notes:

- Explain that the GUI highlights each stage of the pipeline.
- If an error happens, the failed stage is highlighted and execution stops.
- Mention that each stage has waiting, active, passed, and failed states.

## Slide 5: Lexical Analysis

Content:

- The lexer converts characters into tokens
- Tokens include type, value, line, and column
- The GUI displays tokens in a table

Speaker Notes:

- Show the Tokens tab in the GUI.
- Explain why line and column are useful for errors.

## Slide 6: Token Table

Content:

```text
Token Type    Token Value    Line    Column
INT           int            1       1
IDENTIFIER    x              1       5
ASSIGN        =              1       7
INTEGER       5              1       9
```

Speaker Notes:

- Explain that the token table is easier to read than a plain list.
- It makes lexical analysis more visual for beginners.

## Slide 7: Syntax Analysis

Content:

- Recursive descent parser
- Reads tokens in grammar order
- Builds an Abstract Syntax Tree

Speaker Notes:

- Explain that syntax analysis checks structure.
- Mention that missing semicolons and missing braces are syntax errors.

## Slide 8: AST Visualization

Content:

```text
Program
  Declaration
    Type: int
    Name: x
    Value:
      Integer: 5
```

Speaker Notes:

- Show the AST tab.
- Explain how nested indentation represents the tree.

## Slide 9: Semantic Analysis

Content:

- Checks meaning after syntax is valid
- Uses a symbol table
- Checks declaration before use
- Checks type compatibility
- Checks boolean conditions

Speaker Notes:

- Explain that semantic analysis catches errors like assigning `true` to an `int`.

## Slide 10: Symbol Table

Content:

```text
Variable    Type    Value
x           int     5
result      int     25
isLarge     bool    true
```

Speaker Notes:

- Show the Semantic Analysis tab.
- Explain that values appear after execution.

## Slide 11: Interpreter

Content:

- Walks through the AST
- Stores variables in memory
- Evaluates expressions
- Runs conditions, loops, and print statements

Speaker Notes:

- Explain that interpretation only happens after all compiler checks pass.

## Slide 12: Intermediate Code

Content:

```text
t1 = y * 2
t2 = x + t1
result = t2
```

Speaker Notes:

- Explain that intermediate code is easier for a compiler to optimize than the original source code.
- Mention that this step was added as an extra learning phase inspired by compiler lab work.

## Slide 13: Code Optimization

Content:

```text
Before: t1 = 10 * 2
After:  t1 = 20
```

Speaker Notes:

- Explain constant folding and removal of simple useless instructions.
- Emphasize that the optimization is intentionally beginner-friendly.

## Slide 14: Machine Language

Content:

```text
LOAD y
MUL 2
STORE t1
LOAD t1
STORE result
```

Speaker Notes:

- Explain that VisuLang uses educational assembly-style machine code.
- Clarify that it demonstrates the idea of target code generation, not real CPU binary.

## Slide 15: Execution Trace

Content:

```text
Declared variable x = 5
Evaluated expression y * 2 = 20
Assigned result = 25
Condition result > 20 evaluated to true
Printed 25
```

Speaker Notes:

- Show the Execution Trace tab.
- Explain that the trace helps students understand what the interpreter is doing.

## Slide 16: Step-by-Step Mode

Content:

- Click 1: Lexical Analysis
- Click 2: Syntax Analysis / AST
- Click 3: Semantic Analysis
- Click 4: Intermediate Code
- Click 5: Optimization
- Click 6: Machine Language
- Click 7: Execution and Output

Speaker Notes:

- Demonstrate `Run Step by Step`.
- Pause after each click and explain the visible result.

## Slide 17: Error Handling

Content:

```text
Syntax Error:
Location: line 2, column 1
Message: Missing semicolon after declaration.
Suggestion: Add ';' at the end of the declaration.
```

Speaker Notes:

- Show lexical, syntax, and semantic error examples.
- Point out that the GUI stops at the correct phase.

## Slide 18: Demo Plan

Content:

1. Run valid program in command-line mode
2. Open VisuLang GUI
3. Run the same program normally
4. Run it step by step
5. Show intermediate code, optimized code, and machine language tabs
6. Load invalid examples and show error messages

Speaker Notes:

- This slide is the presenter checklist.

## Slide 19: Why VisuLang Is Special

Content:

- More than a normal compiler assignment
- Shows the pipeline visually with a modern PySide6 interface
- Uses tables and trees
- Adds intermediate code, optimization, and machine language views
- Includes interpreter trace
- Good for screenshots and classroom explanation

Speaker Notes:

- Explain that the project is designed as a teaching tool.

## Slide 20: Conclusion

Content:

- VisuLang keeps the MiniLang compiler working
- Adds visual learning features
- Demonstrates lexical, syntax, semantic, code generation, optimization, machine language, and execution phases clearly

Speaker Notes:

- End by saying VisuLang connects compiler theory to a working, visual classroom demo.
