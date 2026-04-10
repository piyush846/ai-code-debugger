from pathlib import Path
from aidbg.agents.analyser import analyse
from aidbg.agents.compiler import run as compiler_run
from aidbg.agents.fixer import fix
from aidbg.agents.explainer import explain
from aidbg.tools.patcher import apply_fix


def debug(filepath: str, max_attempts: int = 4) -> dict:
    """
    Orchestrator: coordinates all agents in sequence.

    Flow:
      1. Read file
      2. Analyse (language + error type)
      3. Compiler agent validates
      4. If invalid → Fixer agent generates fix (with stderr fed back in)
      5. Repeat up to max_attempts
      6. On success → Explainer summarises the change
      7. Apply fix to file
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

    for attempt in range(1, max_attempts + 1):
        print(f"\n[orchestrator] Attempt {attempt} of {max_attempts}")

        result = compiler_run(code, language)

        if result.success:
            if attempt == 1:
                return {"status": "ok", "message": "No errors found. Code is valid."}

            # Code was fixed — explain and apply
            explanation = explain(original_code, code, language, last_stderr)
            apply_fix(filepath, code)

            return {
                "status": "fixed",
                "attempts": attempt - 1,
                "explanation": explanation,
            }

        last_stderr = result.stderr

        # BUG FIX: stderr is now passed to fixer so LLM gets compiler feedback
        fixed_code = fix(code, language, error_type, stderr=last_stderr)

        if fixed_code is None:
            print("[orchestrator] Fixer returned nothing, retrying...")
            continue

        code = fixed_code  # update for next iteration

    return {
        "status": "failed",
        "message": f"Could not fix after {max_attempts} attempts.",
        "last_error": last_stderr,
    }