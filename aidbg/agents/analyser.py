from pathlib import Path

SYSTEM = """You are a code analysis expert.
Your ONLY job is to detect the programming language and classify the error type.
You do NOT fix code. You do NOT explain concepts."""


def detect_language(code: str, filename: str | None = None) -> str:
    if filename:
        suffix = Path(filename).suffix.lower()
        if suffix == ".py":
            return "python"
        if suffix == ".js":
            return "javascript"
        if suffix in (".cpp", ".cc", ".cxx"):
            return "c++"
        if suffix == ".c":
            return "c"
        if suffix == ".java":
            return "java"

    code_lower = code.lower()
    if "def " in code_lower:
        return "python"
    if "#include" in code_lower:
        return "c++"
    if "public static void main" in code_lower:
        return "java"
    if "console.log" in code_lower:
        return "javascript"

    return "unknown"


def classify_error(code: str) -> str:
    code_lower = code.lower()
    if "def" in code_lower and ":" not in code_lower:
        return "Possible Python syntax error (missing colon)"
    if "while(true)" in code_lower:
        return "Possible infinite loop"
    if "int" in code_lower and ";" not in code_lower:
        return "Possible missing semicolon"
    return "Unknown or logical error"


def analyse(code: str, filename: str | None = None) -> dict:
    language = detect_language(code, filename)
    error_type = classify_error(code)
    return {"language": language, "error_type": error_type}