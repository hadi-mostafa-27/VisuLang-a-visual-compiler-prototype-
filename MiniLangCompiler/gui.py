"""PySide6 dashboard for VisuLang, the visual MiniLang compiler."""

import os
import sys

from code_generator import (
    CodeOptimizer,
    IntermediateCodeGenerator,
    MachineCodeGenerator,
    format_numbered_lines,
)
from errors import LexicalError, ParserError, RuntimeMiniLangError, SemanticError
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

try:
    from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, QTimer
    from PySide6.QtGui import QColor, QFont, QPalette
    from PySide6.QtWidgets import (
        QApplication,
        QAbstractItemView,
        QFileDialog,
        QFrame,
        QGraphicsOpacityEffect,
        QGridLayout,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QMainWindow,
        QMessageBox,
        QPlainTextEdit,
        QPushButton,
        QSizePolicy,
        QSplitter,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError as import_error:
    PYSIDE6_IMPORT_ERROR = import_error
else:
    PYSIDE6_IMPORT_ERROR = None


APP_TITLE = "VisuLang: A Visual Compiler for Learning Programming Languages"
PIPELINE_STAGES = [
    "Source",
    "Lexer",
    "Parser",
    "Semantic",
    "IR",
    "Optimize",
    "Machine",
    "Interpreter",
    "Output",
]

DEFAULT_PROGRAM = """int x = 5;
int y = 10;
int result;

result = x + y * 2;

if (result > 20) {
    print(result);
} else {
    print(0);
}

while (x < 10) {
    x = x + 1;
    print(x);
}
"""


if PYSIDE6_IMPORT_ERROR is None:

    class PipelineStageCard(QFrame):
        """Small animated card used in the compiler pipeline."""

        COLORS = {
            "waiting": ("#1B2636", "#8FA3B8", "#26364A"),
            "active": ("#2B6CB0", "#FFFFFF", "#63B3ED"),
            "passed": ("#1F7A4D", "#FFFFFF", "#68D391"),
            "failed": ("#A83246", "#FFFFFF", "#FC8181"),
        }

        def __init__(self, title):
            super().__init__()
            self.title = title
            self.state = "waiting"
            self.pulse_on = False
            self.setObjectName("PipelineStageCard")
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.setMinimumHeight(74)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(14, 10, 14, 10)
            layout.setSpacing(3)

            self.title_label = QLabel(title)
            self.title_label.setObjectName("PipelineTitle")
            self.status_label = QLabel("Waiting")
            self.status_label.setObjectName("PipelineStatus")
            layout.addWidget(self.title_label)
            layout.addWidget(self.status_label)

            self.set_state("waiting")

        def set_state(self, state):
            self.state = state
            self.status_label.setText(state.capitalize())
            bg, fg, border = self.COLORS[state]
            self.setStyleSheet(
                f"""
                QFrame#PipelineStageCard {{
                    background-color: {bg};
                    border: 1px solid {border};
                    border-radius: 14px;
                }}
                QLabel#PipelineTitle {{
                    color: {fg};
                    font-size: 14px;
                    font-weight: 700;
                }}
                QLabel#PipelineStatus {{
                    color: {fg};
                    font-size: 11px;
                }}
                """
            )

        def pulse(self):
            if self.state != "active":
                return
            self.pulse_on = not self.pulse_on
            border = "#BEE3F8" if self.pulse_on else "#63B3ED"
            self.setStyleSheet(
                f"""
                QFrame#PipelineStageCard {{
                    background-color: #2B6CB0;
                    border: 2px solid {border};
                    border-radius: 14px;
                }}
                QLabel#PipelineTitle {{
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: 700;
                }}
                QLabel#PipelineStatus {{
                    color: #FFFFFF;
                    font-size: 11px;
                }}
                """
            )


    class VisuLangWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle(APP_TITLE)
            self.resize(1400, 860)

            self.tokens = None
            self.ast = None
            self.semantic_analyzer = None
            self.interpreter = None
            self.intermediate_code = None
            self.optimized_code = None
            self.machine_code = None
            self.step_index = 0
            self.step_source = None
            self.pipeline_cards = {}

            self.pulse_timer = QTimer(self)
            self.pulse_timer.timeout.connect(self.pulse_active_stage)
            self.pulse_timer.start(650)

            self.build_ui()
            self.apply_theme()
            self.source_editor.setPlainText(DEFAULT_PROGRAM)
            self.reset_pipeline()
            self.current_phase_label.setText("Current phase: Waiting")

        def build_ui(self):
            central = QWidget()
            self.setCentralWidget(central)

            root = QVBoxLayout(central)
            root.setContentsMargins(18, 18, 18, 18)
            root.setSpacing(14)

            root.addWidget(self.create_header())
            root.addWidget(self.create_pipeline())

            splitter = QSplitter(Qt.Horizontal)
            splitter.setObjectName("MainSplitter")
            splitter.addWidget(self.create_editor_card())
            splitter.addWidget(self.create_results_card())
            splitter.setSizes([570, 830])
            root.addWidget(splitter, stretch=1)

        def create_header(self):
            header = QFrame()
            header.setObjectName("HeaderCard")
            layout = QHBoxLayout(header)
            layout.setContentsMargins(22, 18, 22, 18)
            layout.setSpacing(16)

            title_group = QVBoxLayout()
            title = QLabel(APP_TITLE)
            title.setObjectName("AppTitle")
            subtitle = QLabel(
                "Interactive compiler pipeline: Source -> Lexer -> Parser -> Semantic -> IR -> Optimize -> Machine -> Interpreter -> Output"
            )
            subtitle.setObjectName("AppSubtitle")
            title_group.addWidget(title)
            title_group.addWidget(subtitle)

            self.current_phase_label = QLabel("Current phase: Waiting")
            self.current_phase_label.setObjectName("CurrentPhase")
            self.current_phase_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            layout.addLayout(title_group, stretch=1)
            layout.addWidget(self.current_phase_label)
            return header

        def create_pipeline(self):
            frame = QFrame()
            frame.setObjectName("PipelineContainer")
            layout = QHBoxLayout(frame)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            for index, stage in enumerate(PIPELINE_STAGES):
                card = PipelineStageCard(stage)
                self.pipeline_cards[stage] = card
                layout.addWidget(card)
                if index < len(PIPELINE_STAGES) - 1:
                    arrow = QLabel("->")
                    arrow.setObjectName("PipelineArrow")
                    arrow.setAlignment(Qt.AlignCenter)
                    layout.addWidget(arrow)

            return frame

        def create_editor_card(self):
            card = QFrame()
            card.setObjectName("PanelCard")
            layout = QVBoxLayout(card)
            layout.setContentsMargins(18, 18, 18, 18)
            layout.setSpacing(12)

            title = QLabel("Source Code Editor")
            title.setObjectName("SectionTitle")
            layout.addWidget(title)

            self.source_editor = QPlainTextEdit()
            self.source_editor.setObjectName("SourceEditor")
            self.source_editor.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.source_editor.setFont(QFont("Consolas", 11))
            layout.addWidget(self.source_editor, stretch=1)

            buttons = QGridLayout()
            buttons.setSpacing(10)
            self.run_button = QPushButton("Run Compiler")
            self.step_button = QPushButton("Run Step by Step")
            self.reset_steps_button = QPushButton("Reset Steps")
            self.clear_button = QPushButton("Clear")
            self.load_button = QPushButton("Load Example")
            self.save_button = QPushButton("Save Code")

            self.run_button.clicked.connect(self.run_compiler)
            self.step_button.clicked.connect(self.run_step_by_step)
            self.reset_steps_button.clicked.connect(self.reset_steps)
            self.clear_button.clicked.connect(self.clear_all)
            self.load_button.clicked.connect(self.load_example)
            self.save_button.clicked.connect(self.save_code)

            buttons.addWidget(self.run_button, 0, 0)
            buttons.addWidget(self.step_button, 0, 1)
            buttons.addWidget(self.reset_steps_button, 0, 2)
            buttons.addWidget(self.clear_button, 1, 0)
            buttons.addWidget(self.load_button, 1, 1)
            buttons.addWidget(self.save_button, 1, 2)
            layout.addLayout(buttons)

            return card

        def create_results_card(self):
            card = QFrame()
            card.setObjectName("PanelCard")
            layout = QVBoxLayout(card)
            layout.setContentsMargins(18, 18, 18, 18)
            layout.setSpacing(12)

            title = QLabel("Compiler Visualization Dashboard")
            title.setObjectName("SectionTitle")
            layout.addWidget(title)

            self.tabs = QTabWidget()
            self.tabs.setObjectName("ResultTabs")
            layout.addWidget(self.tabs, stretch=1)

            self.create_source_tab()
            self.create_tokens_tab()
            self.create_ast_tab()
            self.create_semantic_tab()
            self.create_intermediate_tab()
            self.create_optimized_tab()
            self.create_machine_tab()
            self.create_trace_tab()
            self.create_errors_tab()
            self.create_output_tab()
            return card

        def create_source_tab(self):
            self.source_view = self.readonly_text()
            self.tabs.addTab(self.source_view, "Source Code")

        def create_tokens_tab(self):
            self.tokens_table = QTableWidget(0, 5)
            self.tokens_table.setObjectName("DataTable")
            self.tokens_table.setHorizontalHeaderLabels(["Index", "Token Type", "Value", "Line", "Column"])
            self.tokens_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tokens_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tokens_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tabs.addTab(self.tokens_table, "Tokens")

        def create_ast_tab(self):
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)

            self.ast_tree = QTreeWidget()
            self.ast_tree.setObjectName("AstTree")
            self.ast_tree.setHeaderLabel("Abstract Syntax Tree")
            self.ast_tree.setAnimated(True)
            layout.addWidget(self.ast_tree, stretch=1)

            self.ast_text = self.readonly_text()
            self.ast_text.setMaximumHeight(150)
            layout.addWidget(self.ast_text)
            self.tabs.addTab(container, "AST")

        def create_semantic_tab(self):
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            self.semantic_status = QLabel("Semantic Analysis: Waiting")
            self.semantic_status.setObjectName("SemanticStatus")
            layout.addWidget(self.semantic_status)

            self.symbol_table = QTableWidget(0, 3)
            self.symbol_table.setObjectName("DataTable")
            self.symbol_table.setHorizontalHeaderLabels(["Variable Name", "Variable Type", "Current Value"])
            self.symbol_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.symbol_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.symbol_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            layout.addWidget(self.symbol_table, stretch=1)
            self.tabs.addTab(container, "Semantic Analysis")

        def create_intermediate_tab(self):
            self.intermediate_view = self.readonly_text()
            self.tabs.addTab(self.intermediate_view, "Intermediate Code")

        def create_optimized_tab(self):
            self.optimized_view = self.readonly_text()
            self.tabs.addTab(self.optimized_view, "Optimized Code")

        def create_machine_tab(self):
            self.machine_view = self.readonly_text()
            self.tabs.addTab(self.machine_view, "Machine Language")

        def create_output_tab(self):
            self.output_view = self.readonly_text()
            self.tabs.addTab(self.output_view, "Program Output")

        def create_trace_tab(self):
            self.trace_view = self.readonly_text()
            self.tabs.addTab(self.trace_view, "Execution Trace")

        def create_errors_tab(self):
            self.errors_view = self.readonly_text()
            self.errors_view.setObjectName("ErrorView")
            self.errors_view.setPlainText("No errors found.")
            self.tabs.addTab(self.errors_view, "Errors")

        def readonly_text(self):
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setFont(QFont("Consolas", 10))
            return text_edit

        def run_compiler(self):
            self.reset_steps(clear_outputs=True)
            source_code = self.begin_new_run()

            try:
                self.tokens = self.run_lexer(source_code)
                self.ast = self.run_parser(self.tokens)
                self.semantic_analyzer = self.run_semantic(self.ast)
                self.intermediate_code = self.run_intermediate_code(self.ast)
                self.optimized_code = self.run_optimizer(self.intermediate_code)
                self.machine_code = self.run_machine_code(self.optimized_code)
                self.interpreter = self.run_interpreter(self.ast, self.semantic_analyzer)
                self.errors_view.setPlainText("No errors found.")
                self.current_phase_label.setText("Current phase: Complete")
            except (LexicalError, ParserError, SemanticError, RuntimeMiniLangError, ValueError) as error:
                self.show_error(error)

        def run_step_by_step(self):
            source_code = self.source_editor.toPlainText().strip()
            if self.step_source != source_code or self.step_index >= 7:
                self.reset_steps(clear_outputs=True)
                self.begin_new_run(source_code)

            try:
                if self.step_index == 0:
                    self.tokens = self.run_lexer(source_code)
                    self.step_index = 1
                    self.current_phase_label.setText("Current phase: Lexical analysis complete")
                    return
                if self.step_index == 1:
                    self.ast = self.run_parser(self.tokens)
                    self.step_index = 2
                    self.current_phase_label.setText("Current phase: Syntax analysis complete")
                    return
                if self.step_index == 2:
                    self.semantic_analyzer = self.run_semantic(self.ast)
                    self.step_index = 3
                    self.current_phase_label.setText("Current phase: Semantic analysis complete")
                    return
                if self.step_index == 3:
                    self.intermediate_code = self.run_intermediate_code(self.ast)
                    self.step_index = 4
                    self.current_phase_label.setText("Current phase: Intermediate code generated")
                    return
                if self.step_index == 4:
                    self.optimized_code = self.run_optimizer(self.intermediate_code)
                    self.step_index = 5
                    self.current_phase_label.setText("Current phase: Optimization complete")
                    return
                if self.step_index == 5:
                    self.machine_code = self.run_machine_code(self.optimized_code)
                    self.step_index = 6
                    self.current_phase_label.setText("Current phase: Machine language generated")
                    return
                if self.step_index == 6:
                    self.interpreter = self.run_interpreter(self.ast, self.semantic_analyzer)
                    self.step_index = 7
                    self.current_phase_label.setText("Current phase: Step-by-step run complete")
            except (LexicalError, ParserError, SemanticError, RuntimeMiniLangError, ValueError) as error:
                self.show_error(error)

        def begin_new_run(self, source_code=None):
            if source_code is None:
                source_code = self.source_editor.toPlainText().strip()
            self.step_source = source_code
            self.source_view.setPlainText(source_code if source_code else "(empty source code)")
            self.errors_view.setPlainText("No errors found.")
            self.set_pipeline_state(passed=["Source"], active="Lexer")
            self.current_phase_label.setText("Current phase: Lexical analysis")
            self.switch_to_tab("Source Code")
            return source_code

        def run_lexer(self, source_code):
            self.set_pipeline_state(passed=["Source"], active="Lexer")
            tokens = Lexer(source_code).scan_tokens()
            self.display_tokens(tokens)
            self.set_pipeline_state(passed=["Source", "Lexer"], active=None)
            self.fade_to_tab("Tokens")
            return tokens

        def run_parser(self, tokens):
            self.set_pipeline_state(passed=["Source", "Lexer"], active="Parser")
            ast = Parser(tokens).parse()
            ast_text = str(ast)
            self.ast_text.setPlainText(ast_text)
            self.populate_ast_tree(ast_text)
            self.set_pipeline_state(passed=["Source", "Lexer", "Parser"], active=None)
            self.fade_to_tab("AST")
            return ast

        def run_semantic(self, ast):
            self.set_pipeline_state(passed=["Source", "Lexer", "Parser"], active="Semantic")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            self.display_semantic(analyzer)
            self.set_pipeline_state(passed=["Source", "Lexer", "Parser", "Semantic"], active=None)
            self.fade_to_tab("Semantic Analysis")
            return analyzer

        def run_intermediate_code(self, ast):
            self.set_pipeline_state(passed=["Source", "Lexer", "Parser", "Semantic"], active="IR")
            intermediate_code = IntermediateCodeGenerator().generate(ast)
            self.intermediate_view.setPlainText(format_numbered_lines(intermediate_code))
            self.set_pipeline_state(passed=["Source", "Lexer", "Parser", "Semantic", "IR"], active=None)
            self.fade_to_tab("Intermediate Code")
            return intermediate_code

        def run_optimizer(self, intermediate_code):
            self.set_pipeline_state(
                passed=["Source", "Lexer", "Parser", "Semantic", "IR"],
                active="Optimize",
            )
            optimized_code = CodeOptimizer().optimize(intermediate_code)
            self.optimized_view.setPlainText(format_numbered_lines(optimized_code))
            self.set_pipeline_state(
                passed=["Source", "Lexer", "Parser", "Semantic", "IR", "Optimize"],
                active=None,
            )
            self.fade_to_tab("Optimized Code")
            return optimized_code

        def run_machine_code(self, optimized_code):
            self.set_pipeline_state(
                passed=["Source", "Lexer", "Parser", "Semantic", "IR", "Optimize"],
                active="Machine",
            )
            machine_code = MachineCodeGenerator().generate(optimized_code)
            self.machine_view.setPlainText(format_numbered_lines(machine_code))
            self.set_pipeline_state(
                passed=["Source", "Lexer", "Parser", "Semantic", "IR", "Optimize", "Machine"],
                active=None,
            )
            self.fade_to_tab("Machine Language")
            return machine_code

        def run_interpreter(self, ast, analyzer):
            self.set_pipeline_state(
                passed=["Source", "Lexer", "Parser", "Semantic", "IR", "Optimize", "Machine"],
                active="Interpreter",
            )
            interpreter = Interpreter(trace_enabled=True)
            output = interpreter.interpret(ast)
            self.output_view.setPlainText("\n".join(output) if output else "(program finished with no output)")
            trace = interpreter.get_trace()
            trace_text = "\n".join(f"{index + 1}. {line}" for index, line in enumerate(trace))
            self.trace_view.setPlainText(trace_text if trace_text else "(no execution trace)")
            self.display_semantic(analyzer, interpreter.memory_snapshot())
            self.set_pipeline_state(
                passed=[
                    "Source",
                    "Lexer",
                    "Parser",
                    "Semantic",
                    "IR",
                    "Optimize",
                    "Machine",
                    "Interpreter",
                ],
                active="Output",
            )
            self.set_pipeline_state(passed=PIPELINE_STAGES, active=None)
            self.fade_to_tab("Program Output")
            return interpreter

        def display_tokens(self, tokens):
            self.tokens_table.setRowCount(0)
            for index, token in enumerate(tokens):
                row = self.tokens_table.rowCount()
                self.tokens_table.insertRow(row)
                values = [
                    str(index),
                    token.token_type,
                    str(token.value),
                    str(getattr(token, "line", "-")),
                    str(getattr(token, "column", "-")),
                ]
                for column, value in enumerate(values):
                    self.tokens_table.setItem(row, column, QTableWidgetItem(value))

        def populate_ast_tree(self, ast_text):
            self.ast_tree.clear()
            stack = []

            for raw_line in ast_text.splitlines():
                if not raw_line.strip():
                    continue
                level = (len(raw_line) - len(raw_line.lstrip(" "))) // 2
                item = QTreeWidgetItem([raw_line.strip()])

                if level == 0:
                    self.ast_tree.addTopLevelItem(item)
                    stack = [item]
                    continue

                while len(stack) > level:
                    stack.pop()
                if stack:
                    stack[-1].addChild(item)
                else:
                    self.ast_tree.addTopLevelItem(item)
                stack.append(item)

            self.ast_tree.expandAll()

        def display_semantic(self, analyzer, values=None):
            values = values or {}
            self.set_semantic_status("Semantic Analysis: Passed", "passed")

            self.symbol_table.setRowCount(0)
            rows = analyzer.symbol_table_rows()
            if not rows:
                rows = [("(empty)", "", "")]

            for name, var_type in rows:
                value = values.get(name, "Not executed yet") if name != "(empty)" else ""
                if isinstance(value, bool):
                    value = "true" if value else "false"
                row = self.symbol_table.rowCount()
                self.symbol_table.insertRow(row)
                for column, table_value in enumerate([name, var_type, str(value)]):
                    self.symbol_table.setItem(row, column, QTableWidgetItem(table_value))

        def show_error(self, error):
            failed_stage = self.stage_for_error(error)
            passed = self.passed_before(failed_stage)
            self.set_pipeline_state(passed=passed, failed=failed_stage)

            message = self.format_error(error)
            self.errors_view.setPlainText(message)
            if failed_stage == "Semantic":
                self.set_semantic_status("Semantic Analysis: Failed", "failed")
            elif self.semantic_analyzer is not None:
                self.set_semantic_status("Semantic Analysis: Passed", "passed")
            else:
                self.set_semantic_status("Semantic Analysis: Waiting", "waiting")
            self.fade_to_tab("Errors")
            self.animate_error_panel()
            self.current_phase_label.setText(f"Current phase: {failed_stage} failed")

        def format_error(self, error):
            if hasattr(error, "to_display"):
                return error.to_display()
            if isinstance(error, ValueError):
                return (
                    "Code Generation Error:\n"
                    f"Message: {error}\n"
                    "Suggestion: Check that the source program uses supported MiniLang statements."
                )
            return str(error)

        def stage_for_error(self, error):
            if isinstance(error, LexicalError):
                return "Lexer"
            if isinstance(error, ParserError):
                return "Parser"
            if isinstance(error, SemanticError):
                return "Semantic"
            if isinstance(error, RuntimeMiniLangError):
                return "Interpreter"
            if isinstance(error, ValueError):
                return "IR"
            return "Output"

        def passed_before(self, stage):
            if stage not in PIPELINE_STAGES:
                return []
            return PIPELINE_STAGES[: PIPELINE_STAGES.index(stage)]

        def reset_steps(self, clear_outputs=False):
            self.step_index = 0
            self.step_source = None
            self.tokens = None
            self.ast = None
            self.semantic_analyzer = None
            self.interpreter = None
            self.intermediate_code = None
            self.optimized_code = None
            self.machine_code = None
            self.current_phase_label.setText("Current phase: Waiting")
            self.reset_pipeline()
            if clear_outputs:
                self.clear_outputs()

        def clear_all(self):
            self.source_editor.clear()
            self.reset_steps(clear_outputs=True)
            self.errors_view.setPlainText("No errors found.")

        def clear_outputs(self):
            self.source_view.clear()
            self.tokens_table.setRowCount(0)
            self.ast_tree.clear()
            self.ast_text.clear()
            self.set_semantic_status("Semantic Analysis: Waiting", "waiting")
            self.symbol_table.setRowCount(0)
            self.intermediate_view.clear()
            self.optimized_view.clear()
            self.machine_view.clear()
            self.trace_view.clear()
            self.errors_view.setPlainText("No errors found.")
            self.output_view.clear()

        def set_semantic_status(self, text, state):
            self.semantic_status.setText(text)
            self.semantic_status.setProperty("state", state)
            self.semantic_status.style().unpolish(self.semantic_status)
            self.semantic_status.style().polish(self.semantic_status)

        def load_example(self):
            examples_dir = os.path.join(os.path.dirname(__file__), "examples")
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load MiniLang Example",
                examples_dir,
                "MiniLang files (*.minilang);;All files (*.*)",
            )
            if not file_path:
                return
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.source_editor.setPlainText(file.read())
            except OSError as error:
                QMessageBox.critical(self, "Load Error", str(error))
            self.reset_steps(clear_outputs=True)

        def save_code(self):
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save MiniLang Code",
                "",
                "MiniLang files (*.minilang);;All files (*.*)",
            )
            if not file_path:
                return
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.source_editor.toPlainText().rstrip() + "\n")
            except OSError as error:
                QMessageBox.critical(self, "Save Error", str(error))

        def reset_pipeline(self):
            for card in self.pipeline_cards.values():
                card.set_state("waiting")

        def set_pipeline_state(self, passed=None, active=None, failed=None):
            passed = passed or []
            for stage, card in self.pipeline_cards.items():
                if stage in passed:
                    card.set_state("passed")
                elif stage == active:
                    card.set_state("active")
                elif stage == failed:
                    card.set_state("failed")
                else:
                    card.set_state("waiting")
            if active:
                self.current_phase_label.setText(f"Current phase: {active}")
            QApplication.processEvents()

        def pulse_active_stage(self):
            for card in self.pipeline_cards.values():
                card.pulse()

        def switch_to_tab(self, name):
            index = self.find_tab(name)
            if index >= 0:
                self.tabs.setCurrentIndex(index)

        def fade_to_tab(self, name):
            self.switch_to_tab(name)
            widget = self.tabs.currentWidget()
            if widget is None:
                return

            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity", self)
            animation.setDuration(260)
            animation.setStartValue(0.15)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.finished.connect(lambda: widget.setGraphicsEffect(None))
            animation.start()
            self._last_fade_animation = animation

        def animate_error_panel(self):
            widget = self.errors_view
            start = widget.pos()
            animation = QPropertyAnimation(widget, b"pos", self)
            animation.setDuration(260)
            animation.setKeyValueAt(0.0, start)
            animation.setKeyValueAt(0.2, start + QPoint(10, 0))
            animation.setKeyValueAt(0.4, start + QPoint(-10, 0))
            animation.setKeyValueAt(0.6, start + QPoint(7, 0))
            animation.setKeyValueAt(0.8, start + QPoint(-7, 0))
            animation.setKeyValueAt(1.0, start)
            animation.setEasingCurve(QEasingCurve.OutQuad)
            animation.start()
            self._last_error_animation = animation

        def find_tab(self, name):
            for index in range(self.tabs.count()):
                if self.tabs.tabText(index) == name:
                    return index
            return -1

        def apply_theme(self):
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor("#0B1120"))
            palette.setColor(QPalette.WindowText, QColor("#E5EEF7"))
            palette.setColor(QPalette.Base, QColor("#101827"))
            palette.setColor(QPalette.AlternateBase, QColor("#162235"))
            palette.setColor(QPalette.Text, QColor("#E5EEF7"))
            palette.setColor(QPalette.Button, QColor("#1F2A3D"))
            palette.setColor(QPalette.ButtonText, QColor("#E5EEF7"))
            QApplication.instance().setPalette(palette)

            self.setStyleSheet(
                """
                QMainWindow {
                    background: #0B1120;
                }
                QFrame#HeaderCard, QFrame#PanelCard {
                    background: #111827;
                    border: 1px solid #253247;
                    border-radius: 18px;
                }
                QLabel#AppTitle {
                    color: #F8FAFC;
                    font-size: 24px;
                    font-weight: 800;
                }
                QLabel#AppSubtitle, QLabel#CurrentPhase {
                    color: #9DB0C7;
                    font-size: 13px;
                }
                QLabel#SectionTitle {
                    color: #F8FAFC;
                    font-size: 16px;
                    font-weight: 700;
                }
                QLabel#PipelineArrow {
                    color: #64748B;
                    font-size: 18px;
                    font-weight: 700;
                }
                QPlainTextEdit#SourceEditor, QTextEdit {
                    background: #0F172A;
                    color: #DDEAF8;
                    border: 1px solid #26364A;
                    border-radius: 14px;
                    padding: 12px;
                    selection-background-color: #2563EB;
                }
                QTextEdit#ErrorView {
                    color: #FECACA;
                    border: 1px solid #7F1D1D;
                }
                QPushButton {
                    background: #1E3A5F;
                    color: #F8FAFC;
                    border: 1px solid #2F5C8A;
                    border-radius: 12px;
                    padding: 10px 12px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background: #26547E;
                    border-color: #60A5FA;
                }
                QPushButton:pressed {
                    background: #1D4ED8;
                }
                QTabWidget::pane {
                    border: 1px solid #26364A;
                    border-radius: 14px;
                    background: #101827;
                    top: -1px;
                }
                QTabBar::tab {
                    background: #172033;
                    color: #9DB0C7;
                    padding: 10px 14px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    margin-right: 3px;
                }
                QTabBar::tab:selected {
                    background: #2563EB;
                    color: #FFFFFF;
                }
                QTableWidget, QTreeWidget {
                    background: #0F172A;
                    alternate-background-color: #152033;
                    color: #DDEAF8;
                    border: 1px solid #26364A;
                    border-radius: 14px;
                    gridline-color: #26364A;
                    selection-background-color: #1D4ED8;
                }
                QHeaderView::section {
                    background: #1E293B;
                    color: #E5EEF7;
                    border: none;
                    padding: 8px;
                    font-weight: 700;
                }
                QLabel#SemanticStatus {
                    background: #1E293B;
                    color: #E5EEF7;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    padding: 12px;
                    font-weight: 700;
                }
                QLabel#SemanticStatus[state="passed"] {
                    background: #14532D;
                    color: #DCFCE7;
                    border: 1px solid #22C55E;
                }
                QLabel#SemanticStatus[state="failed"] {
                    background: #7F1D1D;
                    color: #FECACA;
                    border: 1px solid #EF4444;
                }
                QSplitter::handle {
                    background: #1E293B;
                    width: 6px;
                }
                """
            )


def main():
    if PYSIDE6_IMPORT_ERROR is not None:
        print("PySide6 is required to run the VisuLang GUI.")
        print("Install it with: pip install PySide6")
        print(f"Original import error: {PYSIDE6_IMPORT_ERROR}")
        return 1

    app = QApplication(sys.argv)
    window = VisuLangWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
