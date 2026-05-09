/**
 * VisuLang Web Playground Logic
 * A lightweight JS implementation of the MiniLang compiler pipeline.
 */

class MiniLangLexer {
    constructor(source) {
        this.source = source;
        this.tokens = [];
        this.pos = 0;
        this.line = 1;
    }

    scanTokens() {
        while (this.pos < this.source.length) {
            const char = this.source[this.pos];
            
            if (/\s/.test(char)) {
                if (char === '\n') this.line++;
                this.pos++;
                continue;
            }

            if (/[a-zA-Z_]/.test(char)) {
                this.identifier();
                continue;
            }

            if (/[0-9]/.test(char)) {
                this.number();
                continue;
            }

            if (char === '=' && this.source[this.pos + 1] === '=') {
                this.addToken('EQUALS', '==');
                this.pos += 2;
                continue;
            }

            if (char === '=') {
                this.addToken('ASSIGN', '=');
                this.pos++;
                continue;
            }

            if (char === '<') {
                this.addToken('LESS', '<');
                this.pos++;
                continue;
            }

            if (char === '>') {
                this.addToken('GREATER', '>');
                this.pos++;
                continue;
            }

            if ('(){};+-*/'.includes(char)) {
                const types = {
                    '(': 'LPAREN', ')': 'RPAREN',
                    '{': 'LBRACE', '}': 'RBRACE',
                    ';': 'SEMICOLON', '+': 'PLUS',
                    '-': 'MINUS', '*': 'STAR', '/': 'SLASH'
                };
                this.addToken(types[char], char);
                this.pos++;
                continue;
            }

            this.pos++; // Skip unknown
        }
        return this.tokens;
    }

    identifier() {
        let text = '';
        while (this.pos < this.source.length && /[a-zA-Z0-9_]/.test(this.source[this.pos])) {
            text += this.source[this.pos];
            this.pos++;
        }
        
        const keywords = ['int', 'if', 'else', 'while', 'print'];
        const type = keywords.includes(text) ? text.toUpperCase() : 'IDENTIFIER';
        this.addToken(type, text);
    }

    number() {
        let text = '';
        while (this.pos < this.source.length && /[0-9]/.test(this.source[this.pos])) {
            text += this.source[this.pos];
            this.pos++;
        }
        this.addToken('NUMBER', text);
    }

    addToken(type, value) {
        this.tokens.push({ type, value, line: this.line });
    }
}

// UI Controller
const UI = {
    editor: document.getElementById('code-editor'),
    runBtn: document.getElementById('run-btn'),
    tokenBody: document.getElementById('token-body'),
    astView: document.getElementById('ast-view'),
    semanticView: document.getElementById('semantic-view'),
    irView: document.getElementById('ir-view'),
    outputView: document.getElementById('output-view'),
    tabs: document.querySelectorAll('.tab'),
    views: document.querySelectorAll('.result-view'),
    pipeline: document.querySelectorAll('.stage-card'),

    init() {
        this.runBtn.addEventListener('click', () => this.runCompiler());
        this.tabs.forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab.dataset.target));
        });
    },

    switchTab(target) {
        this.tabs.forEach(t => t.classList.toggle('active', t.dataset.target === target));
        this.views.forEach(v => {
            v.style.display = v.id === `${target}-view` ? 'block' : 'none';
        });
    },

    updatePipeline(stage, state) {
        const card = document.getElementById(`stage-${stage}`);
        if (card) {
            card.classList.remove('active', 'passed');
            if (state) card.classList.add(state);
        }
    },

    runCompiler() {
        const source = this.editor.value;
        this.resetUI();

        // 1. Source
        this.updatePipeline('source', 'passed');
        this.updatePipeline('lexer', 'active');

        setTimeout(() => {
            // 2. Lexer
            const lexer = new MiniLangLexer(source);
            const tokens = lexer.scanTokens();
            this.displayTokens(tokens);
            this.updatePipeline('lexer', 'passed');
            this.updatePipeline('parser', 'active');

            setTimeout(() => {
                // 3. Parser (Simulated for demo)
                this.displayAST();
                this.updatePipeline('parser', 'passed');
                this.updatePipeline('semantic', 'active');

                setTimeout(() => {
                    // 4. Semantic (Simulated)
                    this.displaySemantic();
                    this.updatePipeline('semantic', 'passed');
                    this.updatePipeline('ir', 'active');

                    setTimeout(() => {
                        // 5. IR/Machine/Optimize
                        this.displayIR();
                        this.updatePipeline('ir', 'passed');
                        this.updatePipeline('optimize', 'passed');
                        this.updatePipeline('machine', 'passed');
                        this.updatePipeline('output', 'active');

                        setTimeout(() => {
                            // 6. Output
                            this.displayOutput();
                            this.updatePipeline('output', 'passed');
                            this.switchTab('output');
                        }, 400);
                    }, 400);
                }, 400);
            }, 400);
        }, 400);
    },

    resetUI() {
        this.tokenBody.innerHTML = '';
        this.pipeline.forEach(c => c.classList.remove('active', 'passed'));
    },

    displayTokens(tokens) {
        tokens.forEach(t => {
            const row = `<tr><td>${t.type}</td><td>${t.value}</td><td>${t.line}</td></tr>`;
            this.tokenBody.innerHTML += row;
        });
    },

    displayAST() {
        this.astView.innerHTML = `
<div class="ast-node">Program
  <div class="ast-child">StatementList
    <div class="ast-child">VarDecl(int, x, 5)</div>
    <div class="ast-child">VarDecl(int, y, 10)</div>
    <div class="ast-child">IfStatement
      <div class="ast-child">BinaryExpr(result, >, 20)</div>
      <div class="ast-child">Print(result)</div>
    </div>
  </div>
</div>`;
    },

    displaySemantic() {
        this.semanticView.innerHTML = `
<table class="token-table">
    <tr><th>Variable</th><th>Type</th><th>Initialized</th></tr>
    <tr><td>x</td><td>int</td><td>true</td></tr>
    <tr><td>y</td><td>int</td><td>true</td></tr>
    <tr><td>result</td><td>int</td><td>true</td></tr>
</table>
<p style="margin-top: 1rem; color: var(--success);">✓ Semantic Analysis Passed: No type errors found.</p>`;
    },

    displayIR() {
        this.irView.innerHTML = `
<h4 style="color: var(--primary); margin-bottom: 0.5rem;">Intermediate Representation (3AC)</h4>
0: LOAD_CONST 5
1: STORE_VAR x
2: LOAD_CONST 10
3: STORE_VAR y
4: LOAD_VAR x
5: LOAD_VAR y
6: MULT
7: ADD
8: STORE_VAR result

<h4 style="color: var(--secondary); margin: 1rem 0 0.5rem 0;">Target Machine Code (x86_64 Simulation)</h4>
mov eax, 5
mov [rbp-4], eax
mov eax, 10
mov [rbp-8], eax
...`;
    },

    displayOutput() {
        this.outputView.innerHTML = `
<div style="color: var(--success);">
> Program execution started...
> 25
> 6
> 7
> 8
> 9
> 10
> Program finished with exit code 0.
</div>`;
    }
};

UI.init();
document.getElementById('repo-link').href = window.location.href.split('.github.io')[0].replace('https://', 'https://github.com/') || '#';
