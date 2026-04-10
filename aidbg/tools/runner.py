import subprocess
import tempfile
import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class RunResult:
    success: bool
    stdout: str
    stderr: str


def run_python(code: str) -> RunResult:
    try:
        compile(code, "<string>", "exec")
        return RunResult(success=True, stdout="", stderr="")
    except SyntaxError as e:
        return RunResult(success=False, stdout="", stderr=str(e))


def run_javascript(code: str) -> RunResult:
    try:
        result = subprocess.run(
            ["node", "--check"],
            input=code,
            text=True,
            capture_output=True
        )
        return RunResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr
        )
    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="Node.js not installed")


def run_c(code: str) -> RunResult:
    try:
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        result = subprocess.run(
            ["gcc", "-fsyntax-only", temp_path],
            capture_output=True,
            text=True
        )
        os.remove(temp_path)
        return RunResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr
        )
    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="GCC not installed")


def run_cpp(code: str) -> RunResult:
    try:
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        result = subprocess.run(
            ["g++", "-fsyntax-only", temp_path],
            capture_output=True,
            text=True
        )
        os.remove(temp_path)
        return RunResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr
        )
    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="G++ not installed")


def run_java(code: str) -> RunResult:
    try:
        # BUG FIX: Java requires filename to match class name.
        # Extract class name from code to name the temp file correctly.
        import re
        match = re.search(r'public\s+class\s+(\w+)', code)
        class_name = match.group(1) if match else "Main"

        tmp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(tmp_dir, f"{class_name}.java")

        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            ["javac", temp_path],
            capture_output=True,
            text=True
        )
        os.remove(temp_path)
        os.rmdir(tmp_dir)
        return RunResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr
        )
    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="Java JDK not installed")


def validate_code(code: str, language: str) -> RunResult:
    # BUG FIX: normalise language string so "C/C++" and "c++" both work
    lang = language.lower().strip()

    if lang == "python":
        return run_python(code)
    elif lang == "javascript":
        return run_javascript(code)
    elif lang == "c":
        return run_c(code)
    elif lang in ("c++", "cpp", "c/c++"):
        return run_cpp(code)
    elif lang == "java":
        return run_java(code)
    else:
        print(f"No validator available for: {language}")
        return RunResult(success=True, stdout="", stderr="")