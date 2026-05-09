# VisuLang: Interactive MiniLang Compiler

VisuLang is a visual education platform designed to demystify the inner workings of modern compilers. By providing a step-by-step visualization of the compilation pipeline—from Lexical Analysis to Machine Code generation—VisuLang helps students and developers understand how code is transformed and executed.

![VisuLang Web Interface](visulang_web_mockup.png)

## 🚀 Key Features

- **Live Pipeline Visualization**: Watch as your code flows through the Lexer, Parser, Semantic Analyzer, and Code Generator.
- **Interactive Playground**: Write MiniLang code and see immediate results in the web dashboard.
- **AST Exploration**: Visualize the Abstract Syntax Tree generated from your source code.
- **Machine Code Generation**: See how high-level logic translates into low-level instructions.
- **Integrated Interpreter**: Run your code directly in the environment and see the execution trace.

## 🛠 Compilation Pipeline

1. **Source**: Raw MiniLang code input.
2. **Lexer**: Converts source code into a stream of tokens.
3. **Parser**: Builds an Abstract Syntax Tree (AST) following MiniLang grammar.
4. **Semantic Analysis**: Performs type checking and symbol table management.
5. **IR Generation**: Produces Intermediate Representation (3-Address Code).
6. **Optimizer**: Applies constant folding and dead code elimination.
7. **Machine Code**: Lowers IR to simulated target assembly.
8. **Interpreter**: Executes the code and provides program output.

## 💻 Local Development (Python GUI)

While the web playground provides a quick overview, the full-featured desktop application offers advanced debugging tools.

### Prerequisites
- Python 3.10+
- PySide6

### Setup
```bash
# Clone the repository
git clone https://github.com/your-username/visulang.git

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python MiniLangCompiler/gui.py
```

## 🌐 Live Demo
Visit the [GitHub Pages](https://your-username.github.io/visulang/) to try the interactive playground.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
