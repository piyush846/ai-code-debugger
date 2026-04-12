from aidbg.tools.ollama_client import call_ai

SYSTEM = """You are a code output inspector.
You are given source code and its actual output.
Your job is to determine if the output is logically correct for what the code is trying to do.

Respond ONLY in this exact format:

VERDICT: CORRECT
or
VERDICT: WRONG
REASON: [one sentence explaining what is logically wrong]

No other text. No explanation. Just the verdict."""


def inspect(code: str, language: str, stdout: str, stderr: str) -> dict:
    if stderr and not stdout:
        return {"correct": False, "reason": f"Runtime error: {stderr}"}

    # Empty output is suspicious if code has print statements
    if not stdout and not stderr:
        output_keywords = ["print(", "cout", "System.out", "console.log"]
        if any(kw in code for kw in output_keywords):
            return {
                "correct": False,
                "reason": "Code has print statements but produced no output — possible logic error"
            }
        return {"correct": True, "reason": "No output expected"}

    prompt = f"""This {language} code produced the following output.
Is the output logically correct for what this code is trying to do?

Code:
{code}

Actual output:
{stdout}

Runtime errors (if any):
{stderr if stderr else "None"}"""

    response = call_ai(prompt, system=SYSTEM)

    if not response:
        return {"correct": True, "reason": "Could not inspect output"}

    if "VERDICT: CORRECT" in response.upper():
        return {"correct": True, "reason": "Output is logically correct"}

    if "VERDICT: WRONG" in response.upper():
        lines = response.strip().splitlines()
        reason = ""
        for line in lines:
            if line.upper().startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()
                break
        return {"correct": False, "reason": reason or "Output is logically incorrect"}

    return {"correct": True, "reason": "Could not determine verdict"}