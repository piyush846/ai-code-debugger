from aidbg.tools.ollama_client import call_ai
from aidbg.tools.patcher import extract_fixed_code
from pathlib import Path

SYSTEM = """You are a code repair expert.
Your ONLY job is to fix broken code.
You ALWAYS output in this exact format and nothing else:

ERROR:
[one line describing the bug]

FIXED CODE:
[complete fixed code only]
Rules:
- NEVER use ''' (triple single quotes) as code fences
- ALWAYS use ``` (triple backticks) around the fixed code
- Never explain concepts
- Never add preamble or closing remarks
- Always output the complete fixed file, not just the changed lines
- Start your response with ERROR: immediately"""


def fix(code: str, language: str, error_type: str, stderr: str = "") -> str | None:
    """
    Fixer agent: has its own system prompt identity focused purely on repair.
    Compiler stderr is fed back on every retry so LLM improves each attempt.
    """
    context = f"{error_type}\nCompiler error:\n{stderr}" if stderr else error_type

    prompt = f"""Fix the following {language} code.
Compiler error: {context}

Code to fix:
{code}"""

    output = call_ai(prompt, system=SYSTEM)

    if not output:
        print("[fixer] No response from AI")
        return None

    fixed_code = extract_fixed_code(output)

    if not fixed_code:
        print("[fixer] Could not extract fixed code from AI response")
        print("[fixer] Raw output:\n", output)
        return None

    return fixed_code