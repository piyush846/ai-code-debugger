# aidbg — AI Code Debugger

A multi-agent AI debugging tool that runs fully local using Ollama. Exposes itself as an MCP server so any MCP-compatible client (VS Code, Claude Desktop, or custom agents) can call it as a tool.

PyPI: https://pypi.org/project/aidbg-cli/
GitHub: https://github.com/piyush846/ai-code-debugger

---

## Architecture

aidbg uses a multi-agent architecture where each agent has a focused identity and responsibility:

```
User / MCP Client
      ↓
Orchestrator        ← coordinates agents, manages retry loop
      ↓
Analyser agent      ← detects language, classifies error type (no LLM)
Compiler agent      ← runs real compiler, captures stderr (no LLM)
Fixer agent         ← focused LLM call: repair identity + format enforcement
Explainer agent     ← focused LLM call: explains what was fixed
      ↓
Fixed file + explanation
```

Each LLM-based agent has its own system prompt defining its role. The compiler agent uses the real compiler (gcc/g++/javac/node) — not the LLM — for validation. Compiler stderr is fed back into the fixer on every retry attempt so the model improves with each iteration.

The tool also exposes itself as an **MCP (Model Context Protocol) server**, meaning any MCP-compatible client can call `debug_file` or `analyse_file` as a tool without touching the CLI.

---

## Features

- Fixes Python, C, C++, Java, JavaScript
- Multi-agent pipeline with orchestrator pattern
- Real compiler validation on every attempt (not just LLM guessing)
- Retry loop with stderr feedback — LLM sees actual compiler errors
- Safe fix with automatic `.bak` backup
- MCP server — connect to VS Code, Claude Desktop, or custom agents
- Fully offline — no API keys, no internet required
- Powered by Ollama (qwen2.5-coder:3b recommended)

---

## Install

```bash
pip install aidbg-cli
```

Or clone and install in dev mode:

```bash
git clone https://github.com/piyush846/ai-code-debugger
cd ai-code-debugger
pip install -e .
```

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Pull a model:

```bash
ollama pull qwen2.5-coder:3b
```

- Compilers installed for the languages you want to debug:
  - Python: built-in
  - C/C++: GCC (`gcc`, `g++`)
  - Java: JDK (`javac`)
  - JavaScript: Node.js (`node`)

---

## Usage

### CLI

```bash
# Analyse only (no fix)
aidbg myfile.cpp

# Analyse and auto-fix with backup
aidbg myfile.cpp --fix
```

### Change model

```bash
set AIDBG_MODEL=qwen2.5-coder:3b
aidbg myfile.py --fix
```

### MCP server

Start the MCP server:

```bash
python -m aidbg.mcp.server
```

Connect from a Python MCP client:

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "aidbg.mcp.server"],
        cwd="/path/to/ai-code-debugger"
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "debug_file",
                arguments={"filepath": "/path/to/myfile.cpp"}
            )
            print(result.content[0].text)

asyncio.run(main())
```

### MCP tools exposed

| Tool | Description |
|---|---|
| `debug_file` | Full pipeline — analyse, fix, explain |
| `analyse_file` | Language detection + error classification only |

---

## Connect to VS Code

1. Install the [Continue](https://marketplace.visualstudio.com/items?itemName=Continue.continue) extension in VS Code
2. Press `Ctrl+Shift+P` → `Continue: Open Config`
3. Add aidbg as an MCP server:

```json
{
  "models": [],
  "mcpServers": [
    {
      "name": "aidbg",
      "command": "python",
      "args": ["-m", "aidbg.mcp.server"],
      "cwd": "C:\\path\\to\\ai-code-debugger"
    }
  ]
}
```

4. Restart VS Code
5. Open Continue sidebar (`Ctrl+L`) and type:
   ```
   debug this file: C:\path\to\myfile.cpp
   ```

---

## Project Structure

```
aidbg/
├── cli.py                  # CLI entry point
├── orchestrator.py         # Coordinates all agents, manages retry loop
├── agents/
│   ├── analyser.py         # Language detection + error classification
│   ├── compiler.py         # Real compiler validation
│   ├── fixer.py            # LLM-based code repair agent
│   └── explainer.py        # LLM-based explanation agent
├── tools/
│   ├── runner.py           # Compiler execution (gcc, g++, javac, node)
│   ├── patcher.py          # File patching + backup
│   └── ollama_client.py    # Ollama interface with system prompt support
└── mcp/
    └── server.py           # MCP server exposing debug_file + analyse_file
prompts/
└── debugger.txt            # Fixer prompt template
```

---

## How the retry loop works

```
Attempt 1:
  Compiler runs → fails → stderr captured
  Fixer receives: code + error_type + stderr
  Fixer generates fix → extracted → compiler runs again

Attempt 2:
  Compiler runs on fixed code → still fails → new stderr captured
  Fixer receives: updated code + new stderr
  ...

On success:
  Explainer summarises what was fixed
  Patcher applies fix + creates backup
```

Each retry the fixer sees the latest compiler error — not the original one. This is the key difference from a naive retry loop.

---

## Supported Languages

| Language | Validator |
|---|---|
| Python | `compile()` built-in |
| C | `gcc -fsyntax-only` |
| C++ | `g++ -fsyntax-only` |
| Java | `javac` |
| JavaScript | `node --check` |

---

## License

MIT