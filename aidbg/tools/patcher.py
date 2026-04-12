from pathlib import Path


def extract_fixed_code(ai_output: str) -> str | None:
    lower = ai_output.lower()
    marker = "fixed code:"

    if marker not in lower:
        return None

    idx = lower.index(marker)
    fixed_section = ai_output[idx + len(marker):].strip()

    for fence in ["```", "'''"]:
        if fence in fixed_section:
            parts = fixed_section.split(fence)
            if len(parts) >= 2:
                code_block = parts[1].strip()
                lines = code_block.splitlines()
                if lines:
                    first_line = lines[0].strip().lower()
                    language_labels = ["python", "cpp", "c++", "c", "java", "javascript", "js"]
                    if first_line in language_labels:
                        lines = lines[1:]
                return "\n".join(lines).strip()

    return fixed_section if fixed_section else None


def apply_fix(file_path: str, fixed_code: str) -> None:
    """
    Safely apply fix:
    - Creates a .bak backup of the original
    - Overwrites original with fixed code
    """
    original = Path(file_path).resolve()  # BUG FIX: resolve to absolute path

    backup = original.with_suffix(original.suffix + ".bak")
    backup.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")
    original.write_text(fixed_code, encoding="utf-8")

    print(f"Fix applied successfully")
    print(f"Backup created at: {backup}")