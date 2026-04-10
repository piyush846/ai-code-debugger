from aidbg.tools.runner import validate_code, RunResult

# Compiler agent has no LLM call — its "intelligence" is the actual compiler.
# It runs the code and returns structured feedback to the orchestrator.

def run(code: str, language: str) -> RunResult:
    """
    Compiler agent: validates code using the real compiler.
    Returns RunResult with success flag and stderr for the fixer to use.
    """
    result = validate_code(code, language)

    if result.success:
        print(f"[compiler] Code is valid ({language})")
    else:
        print(f"[compiler] Validation failed ({language})")
        print(f"[compiler] stderr: {result.stderr}")

    return result