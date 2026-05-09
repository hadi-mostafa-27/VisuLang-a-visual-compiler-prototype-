import fs from "node:fs/promises";
import path from "node:path";

const {
  Presentation,
  PresentationFile,
  row,
  column,
  grid,
  panel,
  text,
  rule,
  fill,
  hug,
  fixed,
  grow,
  fr,
  auto,
} = await import("@oai/artifact-tool");

const W = 1920;
const H = 1080;
const TOTAL_SLIDES = 17;

const C = {
  ink: "#12343B",
  ink2: "#31535B",
  paper: "#F6FAF7",
  mint: "#DFF3EA",
  green: "#2E8B57",
  amber: "#F2B84B",
  coral: "#D65050",
  blue: "#3C7DAD",
  plum: "#5B4B8A",
  codeBg: "#0D1F24",
  codeText: "#EAF8F0",
  softLine: "#C7D8D0",
  white: "#FFFFFF",
};

const FONT_HEAD = "Aptos Display";
const FONT_BODY = "Aptos";
const FONT_CODE = "Consolas";

const presentation = Presentation.create({
  slideSize: { width: W, height: H },
});

function t(value, options = {}) {
  return text(value, {
    name: options.name,
    width: options.width ?? fill,
    height: options.height ?? hug,
    columnSpan: options.columnSpan,
    rowSpan: options.rowSpan,
    style: {
      fontFace: options.fontFace ?? FONT_BODY,
      fontSize: options.fontSize ?? 30,
      bold: options.bold ?? false,
      color: options.color ?? C.ink,
      italic: options.italic ?? false,
      ...options.style,
    },
  });
}

function smallLabel(value, color = C.green) {
  return t(value.toUpperCase(), {
    width: hug,
    fontSize: 18,
    bold: true,
    color,
    style: { charSpacing: 3 },
  });
}

function titleStack(title, subtitle = "") {
  const children = [
    smallLabel("MiniLang Compiler / Interpreter"),
    t(title, {
      name: "slide-title",
      fontFace: FONT_HEAD,
      fontSize: 58,
      bold: true,
      color: C.ink,
    }),
  ];
  if (subtitle) {
    children.push(
      t(subtitle, {
        name: "slide-subtitle",
        fontSize: 26,
        color: C.ink2,
        width: fill,
      }),
    );
  }
  return column({ name: "title-stack", width: fill, height: hug, gap: 12 }, children);
}

function footer(index) {
  return row(
    { name: "footer", width: fill, height: hug, align: "center", justify: "between" },
    [
      t("Compiler Design Project", { fontSize: 15, color: "#6A7A78", width: hug }),
      t(`${String(index).padStart(2, "0")} / ${TOTAL_SLIDES}`, {
        fontSize: 15,
        color: "#6A7A78",
        width: hug,
      }),
    ],
  );
}

function addSlide(index, title, subtitle, body, notes) {
  const slide = presentation.slides.add();
  slide.compose(
    panel(
      { name: "background", width: fill, height: fill, fill: C.paper },
      grid(
        {
          name: "slide-root",
          width: fill,
          height: fill,
          rows: [auto, fr(1), auto],
          columns: [fr(1)],
          rowGap: 28,
          padding: { x: 82, y: 58 },
        },
        [titleStack(title, subtitle), body, footer(index)],
      ),
    ),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
  if (notes) slide.speakerNotes.setText(notes);
  return slide;
}

function codeBlock(code, options = {}) {
  return panel(
    {
      name: options.name,
      width: options.width ?? fill,
      height: options.height ?? hug,
      fill: options.fill ?? C.codeBg,
      padding: options.padding ?? { x: 28, y: 24 },
    },
    t(code.trim(), {
      name: options.textName,
      fontFace: FONT_CODE,
      fontSize: options.fontSize ?? 23,
      color: options.color ?? C.codeText,
      width: fill,
    }),
  );
}

function numberedItems(items, accent = C.green) {
  return column(
    { name: "numbered-items", width: fill, height: hug, gap: 20 },
    items.map((item, i) =>
      row(
        { width: fill, height: hug, gap: 18, align: "start" },
        [
          t(String(i + 1).padStart(2, "0"), {
            width: fixed(54),
            fontSize: 24,
            bold: true,
            color: accent,
          }),
          t(item, { fontSize: 29, color: C.ink, width: fill }),
        ],
      ),
    ),
  );
}

function phasePill(label, fillColor, textColor = C.white) {
  return panel(
    {
      width: fill,
      height: fixed(96),
      fill: fillColor,
      padding: { x: 20, y: 22 },
    },
    t(label, {
      fontSize: 25,
      bold: true,
      color: textColor,
      width: fill,
      style: { align: "center" },
    }),
  );
}

function miniPanel(label, value, color = C.green) {
  return column(
    { width: fill, height: hug, gap: 10 },
    [
      t(label, { fontSize: 20, bold: true, color }),
      t(value, { fontSize: 28, color: C.ink }),
    ],
  );
}

function splitTwo(left, right, gap = 42) {
  return grid(
    {
      name: "two-column",
      width: fill,
      height: fill,
      columns: [fr(1), fr(1)],
      columnGap: gap,
      rows: [fr(1)],
    },
    [left, right],
  );
}

function simpleTable(rows, widths = [fr(0.6), fr(1.4)]) {
  return column(
    { width: fill, height: hug, gap: 0 },
    rows.map((cells, index) =>
      grid(
        {
          width: fill,
          height: hug,
          columns: widths,
          columnGap: 18,
          padding: { x: 0, y: 12 },
        },
        cells.map((cell, col) =>
          t(cell, {
            fontSize: index === 0 ? 22 : 24,
            bold: index === 0 || col === 0,
            color: index === 0 ? C.green : C.ink,
          }),
        ),
      ),
    ),
  );
}

function saveNotes(slide, notes) {
  slide.speakerNotes.setText(notes);
}

// Slide 1: custom cover.
{
  const slide = presentation.slides.add();
  slide.compose(
    panel(
      { name: "cover-bg", width: fill, height: fill, fill: C.ink },
      grid(
        {
          name: "cover-root",
          width: fill,
          height: fill,
          rows: [fr(1), auto, auto],
          columns: [fr(1)],
          padding: { x: 100, y: 78 },
          rowGap: 34,
        },
        [
          column(
            { width: fill, height: fill, gap: 20, justify: "center" },
            [
              t("MiniLang", {
                name: "cover-title",
                fontFace: FONT_HEAD,
                fontSize: 118,
                bold: true,
                color: C.white,
              }),
              t("Compiler / Interpreter", {
                name: "cover-subtitle",
                fontFace: FONT_HEAD,
                fontSize: 58,
                bold: true,
                color: C.amber,
              }),
              rule({ width: fixed(360), stroke: C.green, weight: 9 }),
              t("A beginner-friendly Python project that shows tokens, AST, semantic checks, and execution.", {
                fontSize: 31,
                color: "#D8ECE4",
                width: fixed(1260),
              }),
            ],
          ),
          codeBlock(
            `
int x = 5;
print(x);

// Source -> Tokens -> AST -> Checked meaning -> Output
`,
            { fontSize: 27, fill: "#092A31", padding: { x: 32, y: 26 } },
          ),
          row(
            { width: fill, height: hug, justify: "between", align: "center" },
            [
              t("Compiler Design Project", { width: hug, fontSize: 18, color: "#BBD7CD" }),
              t("Python + Tkinter", { width: hug, fontSize: 18, color: "#BBD7CD" }),
            ],
          ),
        ],
      ),
    ),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
  saveNotes(
    slide,
    "Introduce the project as a small programming language called MiniLang. Explain that the project is designed to clearly demonstrate the required compiler phases and then execute valid programs.",
  );
}

addSlide(
  2,
  "Project Objective",
  "Build a simple language that is easy to explain from source code to output.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 28, justify: "center" },
      [
        t("The goal is not to build a huge compiler.", {
          fontFace: FONT_HEAD,
          fontSize: 48,
          bold: true,
          color: C.ink,
        }),
        t("The goal is to make the main compiler phases visible, understandable, and testable.", {
          fontSize: 31,
          color: C.ink2,
        }),
      ],
    ),
    numberedItems([
      "Read MiniLang source code from a file or GUI editor.",
      "Convert source code into tokens using a lexer.",
      "Build an Abstract Syntax Tree using recursive descent parsing.",
      "Check meaning with a symbol table and type rules.",
      "Execute valid programs using a tree-walking interpreter.",
    ]),
  ),
  "Explain that the implementation is pure Python, does not use parser generators, and is intentionally beginner-friendly.",
);

addSlide(
  3,
  "What is MiniLang?",
  "A small educational language with just enough features to feel real.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 18, justify: "center" },
      [
        t("MiniLang supports the language features expected in a small class compiler.", {
          fontFace: FONT_HEAD,
          fontSize: 46,
          bold: true,
          color: C.ink,
        }),
        rule({ width: fixed(280), stroke: C.amber, weight: 7 }),
        t("It includes variables, expressions, conditions, loops, print statements, and comments.", {
          fontSize: 31,
          color: C.ink2,
        }),
      ],
    ),
    grid(
      {
        width: fill,
        height: hug,
        columns: [fr(1), fr(1)],
        columnGap: 24,
        rowGap: 20,
      },
      [
        miniPanel("Types", "int, bool", C.green),
        miniPanel("Statements", "declaration, assignment, print", C.blue),
        miniPanel("Control Flow", "if / else, while", C.plum),
        miniPanel("Expressions", "+ - * / and comparisons", C.coral),
        miniPanel("Comments", "// and /* ... */", C.amber),
        miniPanel("Errors", "lexical, syntax, semantic, runtime", C.green),
      ],
    ),
  ),
  "Describe MiniLang as intentionally small, but complete enough to demonstrate the required compiler concepts.",
);

addSlide(
  4,
  "Compiler Phases",
  "Every program moves through the same pipeline before it can run.",
  column(
    { width: fill, height: fill, gap: 34, justify: "center" },
    [
      row(
        { width: fill, height: hug, gap: 18, align: "center" },
        [
          phasePill("Source Code", C.ink),
          t("->", { width: hug, fontSize: 34, bold: true, color: C.ink2 }),
          phasePill("Lexical Analysis", C.green),
          t("->", { width: hug, fontSize: 34, bold: true, color: C.ink2 }),
          phasePill("Syntax Analysis", C.blue),
        ],
      ),
      row(
        { width: fill, height: hug, gap: 18, align: "center" },
        [
          phasePill("Semantic Analysis", C.plum),
          t("->", { width: hug, fontSize: 34, bold: true, color: C.ink2 }),
          phasePill("Interpretation", C.coral),
          t("->", { width: hug, fontSize: 34, bold: true, color: C.ink2 }),
          phasePill("Program Output", C.amber, C.ink),
        ],
      ),
      t("If any phase finds an error, the compiler stops and displays a clear message.", {
        fontSize: 31,
        bold: true,
        color: C.ink,
        style: { align: "center" },
      }),
    ],
  ),
  "Walk through the pipeline from source code to output. Mention that errors are caught at the appropriate phase.",
);

addSlide(
  5,
  "Lexical Analysis",
  "The lexer reads characters and produces a token stream.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 20 },
      [
        smallLabel("Input"),
        codeBlock(
          `
int x = 5;
print(x);
`,
          { fontSize: 31 },
        ),
        t("Whitespace and comments are ignored. Meaningful parts become tokens.", {
          fontSize: 28,
          color: C.ink2,
        }),
      ],
    ),
    column(
      { width: fill, height: fill, gap: 20 },
      [
        smallLabel("Token Output", C.blue),
        codeBlock(
          `
Token(INT, int)
Token(IDENTIFIER, x)
Token(ASSIGN, =)
Token(INTEGER, 5)
Token(SEMICOLON, ;)
Token(PRINT, print)
Token(LPAREN, ()
Token(IDENTIFIER, x)
Token(RPAREN, ))
Token(SEMICOLON, ;)
Token(EOF, EOF)
`,
          { fontSize: 24, fill: "#112E3A" },
        ),
      ],
    ),
  ),
  "Explain that the lexer recognizes keywords, identifiers, integers, operators, symbols, comments, and EOF.",
);

addSlide(
  6,
  "Syntax Analysis",
  "The parser checks grammar rules and builds an Abstract Syntax Tree.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 22 },
      [
        t("Recursive descent parsing", {
          fontFace: FONT_HEAD,
          fontSize: 45,
          bold: true,
          color: C.ink,
        }),
        numberedItems(
          [
            "Each grammar rule is implemented as a parser method.",
            "The parser consumes tokens in the correct order.",
            "Expressions are parsed with precedence.",
            "The result is an AST used by later phases.",
          ],
          C.blue,
        ),
      ],
    ),
    codeBlock(
      `
Program
  Declaration: int x = 5
    Initializer:
      Integer: 5
  Print
    Identifier: x
`,
      { fontSize: 31, fill: "#102B36" },
    ),
  ),
  "Explain that syntax analysis catches mistakes such as missing semicolons, missing parentheses, or invalid statement order.",
);

addSlide(
  7,
  "Grammar",
  "The grammar defines what valid MiniLang programs look like.",
  grid(
    {
      width: fill,
      height: fill,
      columns: [fr(1), fr(1)],
      columnGap: 28,
      rows: [fr(1)],
    },
    [
      codeBlock(
        `
program     -> statement*
statement   -> declaration
             | assignment
             | print_stmt
             | if_stmt
             | while_stmt

declaration -> type IDENTIFIER
               ("=" expression)? ";"
type        -> "int" | "bool"

assignment  -> IDENTIFIER "="
               expression ";"
print_stmt  -> "print" "("
               expression ")" ";"
`,
        { fontSize: 22, fill: "#0F2830" },
      ),
      codeBlock(
        `
if_stmt     -> "if" "(" expression ")"
               block ("else" block)?
while_stmt  -> "while" "(" expression ")"
               block
block       -> "{" statement* "}"

expression  -> equality
equality    -> comparison
               (("==" | "!=") comparison)*
comparison  -> term
               (("<" | ">" | "<=" | ">=") term)*
term        -> factor (("+" | "-") factor)*
factor      -> unary (("*" | "/") unary)*
unary       -> "-" unary | primary
primary     -> INTEGER | true | false
             | IDENTIFIER | "(" expression ")"
`,
        { fontSize: 20, fill: "#0F2830" },
      ),
    ],
  ),
  "Point out that the expression rules create operator precedence, so multiplication is parsed before addition.",
);

addSlide(
  8,
  "Semantic Analysis",
  "This phase checks whether the parsed program makes sense.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 24, justify: "center" },
      [
        t("Syntax can be correct while meaning is wrong.", {
          fontFace: FONT_HEAD,
          fontSize: 46,
          bold: true,
          color: C.ink,
        }),
        codeBlock(
          `
int age = 20;
age = true;
`,
          { fontSize: 32, fill: "#2B1B1B" },
        ),
        t("This is syntactically valid, but semantically invalid.", {
          fontSize: 28,
          bold: true,
          color: C.coral,
        }),
      ],
    ),
    column(
      { width: fill, height: fill, gap: 20, justify: "center" },
      [
        smallLabel("Checks", C.plum),
        numberedItems(
          [
            "Variables must be declared before use.",
            "Variables cannot be declared twice in the same scope.",
            "Assignments must match declared variable types.",
            "if and while conditions must be boolean.",
            "Arithmetic operators only work with integers.",
          ],
          C.plum,
        ),
      ],
    ),
  ),
  "Explain the symbol table and how it stores variable names and their types during semantic analysis.",
);

addSlide(
  9,
  "Interpreter",
  "After successful analysis, the interpreter executes the AST.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 22 },
      [
        t("Execution responsibilities", {
          fontFace: FONT_HEAD,
          fontSize: 44,
          bold: true,
          color: C.ink,
        }),
        numberedItems(
          [
            "Store variable values in memory.",
            "Evaluate expressions.",
            "Run assignments and print statements.",
            "Choose if or else blocks.",
            "Repeat while loop bodies.",
          ],
          C.coral,
        ),
      ],
    ),
    column(
      { width: fill, height: fill, gap: 24, justify: "center" },
      [
        smallLabel("Memory", C.green),
        simpleTable([
          ["Variable", "Value"],
          ["x", "5"],
          ["y", "10"],
          ["result", "25"],
          ["isLarge", "true"],
        ]),
        rule({ width: fill, stroke: C.softLine, weight: 2 }),
        smallLabel("Output", C.amber),
        codeBlock(
          `
25
6
7
8
9
10
`,
          { fontSize: 31, fill: "#173328" },
        ),
      ],
    ),
  ),
  "Explain that the interpreter walks the AST and keeps a runtime memory dictionary for variable values.",
);

addSlide(
  10,
  "Demo Program",
  "The valid example uses declarations, arithmetic, if/else, while, and print.",
  codeBlock(
    `
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
`,
    { fontSize: 24, fill: "#0E252C" },
  ),
  "Use this slide before running the command-line demo. Explain which MiniLang features appear in the program.",
);

addSlide(
  11,
  "Output",
  "The command-line version prints each compiler phase separately.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 24 },
      [
        t("Demo command", {
          fontFace: FONT_HEAD,
          fontSize: 42,
          bold: true,
          color: C.ink,
        }),
        codeBlock(
          `
python main.py examples/valid_program.minilang
`,
          { fontSize: 29, fill: "#153138" },
        ),
        numberedItems(
          [
            "Source Code",
            "Lexical Analysis",
            "Syntax Analysis",
            "Semantic Analysis",
            "Program Output",
          ],
          C.green,
        ),
      ],
    ),
    column(
      { width: fill, height: fill, gap: 18 },
      [
        smallLabel("Program Output", C.amber),
        codeBlock(
          `
25
6
7
8
9
10
`,
          { fontSize: 45, fill: "#173328", padding: { x: 42, y: 34 } },
        ),
        t("This output appears only after lexical, syntax, and semantic analysis succeed.", {
          fontSize: 28,
          color: C.ink2,
        }),
      ],
    ),
  ),
  "Run the valid program from the terminal and point out the labeled output sections.",
);

addSlide(
  12,
  "Error Handling",
  "Different mistakes are caught by different phases.",
  grid(
    {
      width: fill,
      height: fill,
      columns: [fr(1), fr(1), fr(1)],
      columnGap: 24,
      rows: [fr(1)],
    },
    [
      column(
        { width: fill, height: fill, gap: 18 },
        [
          smallLabel("Lexical Error", C.coral),
          codeBlock(
            `
@

Lexical Error:
Invalid character '@'
`,
            { fontSize: 25, fill: "#311A1A" },
          ),
          t("Invalid characters are rejected before parsing starts.", { fontSize: 24, color: C.ink2 }),
        ],
      ),
      column(
        { width: fill, height: fill, gap: 18 },
        [
          smallLabel("Syntax Error", C.blue),
          codeBlock(
            `
int x = 5
print(x);

Syntax Error:
Expected ';'
`,
            { fontSize: 25, fill: "#102B36" },
          ),
          t("Bad grammar is caught while building the AST.", { fontSize: 24, color: C.ink2 }),
        ],
      ),
      column(
        { width: fill, height: fill, gap: 18 },
        [
          smallLabel("Semantic Error", C.plum),
          codeBlock(
            `
int age = 20;
age = true;

Semantic Error:
Cannot assign bool
to int variable 'age'
`,
            { fontSize: 24, fill: "#241D3A" },
          ),
          t("Incorrect meaning is caught after syntax is valid.", { fontSize: 24, color: C.ink2 }),
        ],
      ),
    ],
  ),
  "Demonstrate the three invalid example files and explain why each error belongs to a different phase.",
);

addSlide(
  13,
  "Challenges",
  "The main difficulty was connecting simple rules into a working pipeline.",
  splitTwo(
    numberedItems(
      [
        "Parsing expressions while respecting operator precedence.",
        "Designing AST classes that are easy to read and print.",
        "Keeping semantic checks separate from syntax checks.",
        "Making error messages clear for a class demo.",
        "Reusing the same compiler classes in both CLI and GUI modes.",
      ],
      C.amber,
    ),
    column(
      { width: fill, height: fill, gap: 18, justify: "center" },
      [
        smallLabel("Precedence Ladder", C.blue),
        phasePill("equality: == !=", C.blue),
        phasePill("comparison: < > <= >=", C.green),
        phasePill("term: + -", C.amber, C.ink),
        phasePill("factor: * /", C.coral),
        phasePill("primary: literals, identifiers, (...)", C.plum),
      ],
    ),
  ),
  "Explain that expression parsing was the trickiest part because the parser must understand precedence.",
);

addSlide(
  14,
  "Conclusion",
  "MiniLang proves the complete compiler/interpreter workflow.",
  column(
    { width: fill, height: fill, gap: 34, justify: "center" },
    [
      t("What we built", {
        fontFace: FONT_HEAD,
        fontSize: 48,
        bold: true,
        color: C.ink,
        style: { align: "center" },
      }),
      row(
        { width: fill, height: hug, gap: 18, align: "center" },
        [
          phasePill("Tokens", C.green),
          phasePill("AST", C.blue),
          phasePill("Type Checks", C.plum),
          phasePill("Execution", C.coral),
        ],
      ),
      t("The project connects compiler theory to a working Python program that can be demonstrated from the command line and through a GUI.", {
        fontSize: 32,
        color: C.ink2,
        style: { align: "center" },
      }),
    ],
  ),
  "Summarize the project and emphasize that it demonstrates lexical analysis, syntax analysis, semantic analysis, and interpretation.",
);

addSlide(
  15,
  "GUI Application",
  "The Tkinter GUI visualizes the compiler phases like a small user app.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 24, justify: "center" },
      [
        t("The GUI does not replace main.py.", {
          fontFace: FONT_HEAD,
          fontSize: 46,
          bold: true,
          color: C.ink,
        }),
        t("It reuses the same Lexer, Parser, SemanticAnalyzer, and Interpreter classes.", {
          fontSize: 31,
          color: C.ink2,
        }),
        codeBlock(
          `
python gui.py
`,
          { fontSize: 34, fill: "#153138" },
        ),
      ],
    ),
    panel(
      { width: fill, height: fill, fill: C.white, padding: { x: 24, y: 24 } },
      column(
        { width: fill, height: fill, gap: 16 },
        [
          t("MiniLang Compiler Visualizer", {
            fontSize: 27,
            bold: true,
            color: C.ink,
            style: { align: "center" },
          }),
          codeBlock(
            `
int x = 5;
print(x);
`,
            { fontSize: 26, fill: "#F1F6F3", color: C.ink, padding: { x: 20, y: 18 } },
          ),
          row(
            { width: fill, height: hug, gap: 12 },
            [
              phasePill("Run Compiler", C.green),
              phasePill("Clear", C.blue),
              phasePill("Load Example", C.amber, C.ink),
              phasePill("Save Code", C.plum),
            ],
          ),
          row(
            { width: fill, height: hug, gap: 10 },
            [
              phasePill("Tokens", C.mint, C.ink),
              phasePill("AST", C.mint, C.ink),
              phasePill("Semantic", C.mint, C.ink),
              phasePill("Output", C.mint, C.ink),
              phasePill("Errors", C.mint, C.ink),
            ],
          ),
        ],
      ),
    ),
  ),
  "Open the GUI and explain that it is only the interface layer. The compiler logic remains in the existing compiler classes.",
);

addSlide(
  16,
  "GUI Features",
  "The GUI makes the phases easy to show during a live demo.",
  splitTwo(
    numberedItems(
      [
        "Source code editor with default MiniLang program.",
        "Run Compiler button to start all phases.",
        "Clear, Load Example, and Save Code buttons.",
        "Separate tabs for tokens, AST, semantic analysis, output, and errors.",
        "Errors stop execution and appear in the Errors tab.",
      ],
      C.green,
    ),
    column(
      { width: fill, height: fill, gap: 20, justify: "center" },
      [
        smallLabel("GUI Flow", C.blue),
        phasePill("Source Code Editor", C.ink),
        t("->", { fontSize: 34, bold: true, color: C.ink2, style: { align: "center" } }),
        phasePill("Run Compiler", C.green),
        t("->", { fontSize: 34, bold: true, color: C.ink2, style: { align: "center" } }),
        row(
          { width: fill, height: hug, gap: 12 },
          [
            phasePill("Tokens", C.blue),
            phasePill("AST", C.plum),
            phasePill("Output", C.coral),
          ],
        ),
      ],
    ),
  ),
  "Show the GUI controls and explain what each output tab displays.",
);

addSlide(
  17,
  "GUI Demo",
  "Finish by showing both command-line and GUI execution.",
  splitTwo(
    column(
      { width: fill, height: fill, gap: 24 },
      [
        smallLabel("Command-Line Demo", C.green),
        codeBlock(
          `
python main.py examples/valid_program.minilang
python main.py examples/lexical_error.minilang
python main.py examples/syntax_error.minilang
python main.py examples/semantic_error.minilang
`,
          { fontSize: 25, fill: "#153138" },
        ),
        t("Use the terminal to prove each compiler phase is printed clearly.", {
          fontSize: 27,
          color: C.ink2,
        }),
      ],
    ),
    column(
      { width: fill, height: fill, gap: 24 },
      [
        smallLabel("GUI Demo", C.blue),
        numberedItems(
          [
            "Run python gui.py.",
            "Load or type the valid MiniLang program.",
            "Click Run Compiler.",
            "Show Tokens, AST, Semantic Analysis, Program Output, and Errors tabs.",
            "Load an invalid example to show error handling.",
          ],
          C.blue,
        ),
      ],
    ),
  ),
  "End with the demo plan: first CLI, then GUI. Emphasize that both modes use the same compiler pipeline.",
);

await fs.mkdir("scratch/previews", { recursive: true });
await fs.mkdir("scratch/layouts", { recursive: true });

const pptxBlob = await PresentationFile.exportPptx(presentation);
await pptxBlob.save("output/output.pptx");

for (let i = 0; i < presentation.slides.count; i += 1) {
  const slide = presentation.slides.getItem(i);
  const slideNumber = String(i + 1).padStart(2, "0");
  const preview = await slide.export({ format: "png" });
  await fs.writeFile(`scratch/previews/slide-${slideNumber}.png`, Buffer.from(await preview.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(`scratch/layouts/slide-${slideNumber}.layout.json`, Buffer.from(await layout.arrayBuffer()));
}

const finalDeck = path.resolve("output/output.pptx");

await fs.writeFile(
  "scratch/build-summary.json",
  JSON.stringify(
    {
      slides: presentation.slides.count,
      output: finalDeck,
      previews: path.resolve("scratch/previews"),
      layouts: path.resolve("scratch/layouts"),
    },
    null,
    2,
  ),
);

console.log(`Built ${presentation.slides.count} slides`);
console.log(finalDeck);
