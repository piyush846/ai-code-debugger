from aidbg.tools.ollama_client import call_ai

SYSTEM = """You are a code review assistant.
Your ONLY job is to explain what bug was fixed and why.
Be concise — 2 sentences maximum.
No markdown. No bullet points. Plain text only."""


def explain(original_code: str, fixed_code: str, language: str, stderr: str) -> str:
    """
    Explainer agent: has its own identity focused purely on explanation.
    Called only after a successful fix.
    """
    prompt = f"""A {language} program had this compiler error:
{stderr}

What was the bug and what was changed to fix it?"""

    output = call_ai(prompt, system=SYSTEM)
    return output if output else "Fix applied successfully."