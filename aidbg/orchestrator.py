from pathlib import Path
from aidbg.agents.analyser import analyse
from aidbg.agents.compiler import run as compiler_run
from aidbg.agents.inspector import inspect
from aidbg.agents.fixer import fix
from aidbg.agents.explainer import explain
from aidbg.tools.patcher import apply_fix
from aidbg.tools.runner import validate_code


def debug(filepath: str, max_attempts: int = 4) -> dict:
    """
    Orchestrator: coordinates all agents.

    Flow:
      1. Analyse — language + error type
      2. Compile — syntax check + execute
      3. If syntax error → Fixer with compiler stderr
      4. If runs OK → Inspector checks if output is logically correct
      5. If logic wrong → Fixer with code + wrong output + reason
      6. Repeat up to max_attempts
      7. On success → Explainer + apply fix
    """
    path = Path(filepath).resolve()

    if not path.exists():
        return {"status": "error", "message": f"File not found: {filepath}"}

    code = path.read_text(encoding="utf-8")
    original_code = code

    analysis = analyse(code, filepath)
    language = analysis["language"]
    error_type = analysis["error_type"]

    print(f"[orchestrator] Language: {language}")
    print(f"[orchestrator] Pre-analysis: {error_type}")

    last_stderr = ""
    last_issue = ""

    for attempt in range(1, max_attempts + 1):
        print(f"\n[orchestrator] Attempt {attempt} of {max_attempts}")

        # Step 1 — compile and run
        result = validate_code(code, language)

        # Step 2 — syntax error
        if not result.success and not result.executed:
            print(f"[orchestrator] Syntax error detected")
            last_stderr = result.stderr
            last_issue = f"Syntax error:\n{last_stderr}"

            fixed_code = fix(code, language, error_type, stderr=last_stderr)
            if fixed_code:
                code = fixed_code
            continue

        # Step 3 — runtime error
        if not result.success and result.executed:
            print(f"[orchestrator] Runtime error detected")
            last_stderr = result.stderr
            last_issue = f"Runtime error:\n{last_stderr}"

            fixed_code = fix(code, language, error_type, stderr=last_stderr)
            if fixed_code:
                code = fixed_code
            continue

        # Step 4 — code ran successfully, inspect output
        print(f"[orchestrator] Code executed. Output: {result.stdout[:100]}")
        inspection = inspect(code, language, result.stdout, result.stderr)

        if inspection["correct"]:
            # Code is correct
            if code == original_code:
                return {"status": "ok", "message": "No errors found. Code is valid and output is correct."}

            explanation = explain(original_code, code, language, last_issue)
            apply_fix(filepath, code)
            return {
                "status": "fixed",
                "attempts": attempt,
                "explanation": explanation,
            }

        # Step 5 — logical error
        print(f"[orchestrator] Logic error: {inspection['reason']}")
        last_issue = (
            f"Logical error: {inspection['reason']}\n"
            f"Actual output: {result.stdout}"
        )

        fixed_code = fix(
            code, language, error_type,
            stderr=f"Logic error: {inspection['reason']}\nActual output was: {result.stdout}"
        )
        if fixed_code:
            code = fixed_code

    return {
        "status": "failed",
        "message": f"Could not fix after {max_attempts} attempts.",
        "last_error": last_issue,
    }