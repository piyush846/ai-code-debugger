# aidbg — AI Code Debugger

Fixes syntax errors, runtime errors, and logical errors in your code. Runs fully local — no API keys, no internet required.

---

## What it does

- Runs your code and captures actual output
- Detects if the output is logically wrong — no expected output needed from you
- Fixes the bug automatically
- Explains what was wrong
- Backs up your original file before making any changes

---

## Prerequisites

[Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running. That's it.

---

## Setup

**Step 1 — Download this one file**

Windows (PowerShell):
```bash
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/piyush846/ai-code-debugger/main/docker-compose.yml" -OutFile "docker-compose.yml"
```

Linux/Mac:
```bash
curl -O https://raw.githubusercontent.com/piyush846/ai-code-debugger/main/docker-compose.yml
```

**Step 2 — Start Ollama**
```bash
docker-compose up -d ollama
```

**Step 3 — Pull a model based on your RAM**

| RAM | Command |
|-----|---------|
| 4GB | `docker exec aidbg-ollama ollama pull qwen2.5-coder:1.5b` |
| 8GB | `docker exec aidbg-ollama ollama pull qwen2.5-coder:3b` |
| 16GB | `docker exec aidbg-ollama ollama pull qwen2.5-coder:7b` |

**Step 4 — Create a `workspace` folder next to your `docker-compose.yml` and put your broken file inside it**

```
your-folder/
├── docker-compose.yml
└── workspace/
    └── yourfile.py
```

**Step 5 — Run**
```bash
docker-compose run --rm aidbg python -m aidbg.cli /app/workspace/yourfile.py --fix
```

Your original file is backed up as `yourfile.py.bak` before any changes.

---

## Choosing and changing the model

aidbg uses a local AI model via Ollama to fix your code. The model you choose depends on how much RAM your machine has — bigger models give better results but need more memory.

### Which model should I pick?

| Your RAM | Model | Quality | Speed |
|----------|-------|---------|-------|
| 4GB | `qwen2.5-coder:1.5b` | Good for simple bugs | Fast |
| 8GB | `qwen2.5-coder:3b` | Good for most bugs | Medium |
| 16GB | `qwen2.5-coder:7b` | Great for complex bugs | Slower |
| 32GB | `deepseek-coder:33b` | Best results | Slow |

If you're not sure, start with the model that matches your RAM. If fixes are taking too long or timing out, switch to a smaller one.

### How to change the model

**Step 1 — Pull the model you want** (run this once):
```bash
docker exec aidbg-ollama ollama pull qwen2.5-coder:1.5b
```

**Step 2 — Open `docker-compose.yml` and find this line:**
```yaml
- AIDBG_MODEL=qwen2.5-coder:3b
```

**Step 3 — Change it to your chosen model:**
```yaml
- AIDBG_MODEL=qwen2.5-coder:1.5b
```

**Step 4 — Save the file and run again.** No rebuild needed.

### Change model temporarily (without editing the file)
```bash
docker-compose run --rm -e AIDBG_MODEL=qwen2.5-coder:1.5b aidbg python -m aidbg.cli /app/workspace/yourfile.py --fix
```

---

## VS Code shortcut

Press one key on any open file and aidbg fixes it automatically.

**Step 1** — Press `Ctrl+Shift+P` → type `Open Keyboard Shortcuts JSON` → Enter

**Step 2** — Add this:
```json
[
  {
    "key": "ctrl+b",
    "command": "workbench.action.terminal.sendSequence",
    "args": {
      "text": "docker-compose -f C:\\path\\to\\docker-compose.yml run --rm -v \"${fileDirname}:/app/workspace\" aidbg python -m aidbg.cli /app/workspace/${fileBasename} --fix\n"
    }
  }
]
```

Replace `C:\\path\\to\\docker-compose.yml` with the actual path to your `docker-compose.yml`.

**Step 3** — Open any broken file → press `Ctrl+B`

---

## IntelliJ / PyCharm shortcut

**Step 1** — `File → Settings → Tools → External Tools` → click `+`

| Field | Value |
|-------|-------|
| Name | aidbg |
| Program | docker-compose |
| Arguments | `-f C:\path\to\docker-compose.yml run --rm -v "$FileDir$:/app/workspace" aidbg python -m aidbg.cli /app/workspace/$FileName$ --fix` |
| Working directory | `$ProjectFileDir$` |

**Step 2** — `File → Settings → Keymap` → search `External Tools` → find `aidbg` → right click → `Add Keyboard Shortcut` → press `Ctrl+B`

**Step 3** — Open any broken file → press `Ctrl+B`

---

## Architecture

aidbg is built as a multi-agent pipeline. Instead of one big LLM call that tries to do everything, each agent has a single focused responsibility. This makes the system more reliable — if one agent fails, only that step is retried, not the whole pipeline.

```
User / IDE shortcut
        ↓
  Orchestrator
  Plans the strategy, delegates to agents,
  manages the retry loop (up to 4 attempts)
        ↓
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Analyser agent                                     │
│  No LLM — pure logic                                │
│  Reads the file extension to detect language        │
│  Scans code patterns to classify error type         │
│  Fast and always accurate                           │
│                                                     │
│  Compiler agent                                     │
│  No LLM — uses the real compiler                    │
│  Compiles the code (gcc, g++, javac, node, python)  │
│  If it compiles, actually runs the code             │
│  Captures: stdout, stderr, exit code                │
│  This is what makes aidbg catch runtime errors      │
│  that syntax-only tools miss                        │
│                                                     │
│  Inspector agent                                    │
│  Uses LLM                                           │
│  Reads the source code + actual output together     │
│  Asks: does this output make sense for what         │
│  this code is trying to do?                         │
│  Catches logical bugs — wrong algorithm output,     │
│  missing backtracking, wrong base cases, etc.       │
│  No expected output needed from the user            │
│                                                     │
│  Fixer agent                                        │
│  Uses LLM with repair-focused system prompt         │
│  Receives full context: source code + error type    │
│  + compiler stderr + inspector reason               │
│  + actual wrong output                              │
│  Generates the complete fixed file                  │
│                                                     │
│  Explainer agent                                    │
│  Uses LLM with explanation-focused system prompt    │
│  Summarises what was wrong and what changed         │
│  in plain English                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
        ↓
  Fixed file saved
  Original backed up as .bak
```

### The retry loop

This is what makes aidbg genuinely agentic — it doesn't just try once and give up. Each attempt feeds new information back to the fixer:

```
Attempt 1:
  Compiler runs code → output: "0" (wrong for factorial)
  Inspector reads code + output → detects result initialized to 0
  Fixer receives: code + "result initialized to 0" + actual output "0"
  Fixer generates fix

Attempt 2:
  Compiler runs fixed code → output: "120" (correct)
  Inspector checks → correct
  Fix applied, done
```

If attempt 2 still fails, the fixer gets the new compiler output and inspector feedback from attempt 2 — not the original error. This is why it improves with each retry instead of making the same mistake repeatedly.

### Why separate agents instead of one big prompt?

One big LLM call saying "here's broken code, fix it" works for simple syntax errors but fails for logical errors because the model doesn't know what the code is supposed to output. By splitting into agents:

- The compiler agent actually runs the code — so we have real output, not guessed output
- The inspector agent can compare real output against the code's intent
- The fixer agent gets concrete feedback: "output was 0, should be 120 based on the factorial logic"

This concrete feedback is what allows the fixer to correctly identify `result = 0` as the bug rather than guessing.

### Error types handled

| Error type | Example | Detected by |
|------------|---------|-------------|
| Syntax error | Missing bracket, wrong indentation | Compiler agent |
| Runtime error | Division by zero, index out of range | Compiler agent (execution) |
| Logical error | Wrong algorithm output | Inspector agent |
| Missing backtrack | N-Queens returns "No solution" | Inspector agent |
| Wrong initialisation | Factorial initialised to 0 | Inspector agent |

---

## Supported languages

Python, C, C++, Java, JavaScript

---

## License

MIT