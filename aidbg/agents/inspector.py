from aidbg.tools.ollama_client import call_ai

SYSTEM = """You are a code output inspector.
You are given source code and its actual output.
Your job is to determine if the output is logically correct.

Rules:
- If output is "No solution" but the code is solving a problem that HAS known solutions (like 4-Queens, 8-Queens, sorting, factorial), mark as WRONG
- If output is empty but code has print statements, mark as WRONG
- If output looks like a valid result for what the code does, mark as CORRECT
- For board/grid problems: verify the output makes structural sense

Respond ONLY in this exact format:

VERDICT: CORRECT
or
VERDICT: WRONG
REASON: [one sentence explaining what is logically wrong]

No other text. No explanation. Just the verdict."""


def inspect(code: str, language: str, stdout: str, stderr: str) -> dict:
    if stderr and not stdout:
        return {"correct": False, "reason": f"Runtime error: {stderr}"}
    # No solution from a solver is suspicious
    if stdout.strip().lower() == "no solution":
        return {
        "correct": False,
        "reason": "Code outputs 'No solution' but the problem likely has valid solutions — possible logic error"
    }

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