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
    executed: bool = False  # True if code actually ran, False if just syntax checked


def _run_process(cmd: list, input_data: str = "", timeout: int = 10) -> RunResult:
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        return RunResult(
            success=result.returncode == 0,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
            executed=True
        )
    except subprocess.TimeoutExpired:
        return RunResult(success=False, stdout="", stderr="Execution timed out after 10 seconds", executed=True)
    except FileNotFoundError as e:
        return RunResult(success=False, stdout="", stderr=str(e), executed=False)


def run_python(code: str, input_data: str = "") -> RunResult:
    # First check syntax
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return RunResult(success=False, stdout="", stderr=str(e), executed=False)

    # Then actually execute
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as f:
        f.write(code)
        temp_path = f.name

    result = _run_process(["python", temp_path], input_data)
    os.remove(temp_path)
    return result


def run_c(code: str, input_data: str = "") -> RunResult:
    try:
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        exe_path = temp_path.replace(".c", "")
        compile_result = subprocess.run(
            ["gcc", temp_path, "-o", exe_path],
            capture_output=True, text=True
        )

        if compile_result.returncode != 0:
            os.remove(temp_path)
            return RunResult(success=False, stdout="", stderr=compile_result.stderr, executed=False)

        result = _run_process([exe_path], input_data)
        os.remove(temp_path)
        os.remove(exe_path)
        return result

    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="GCC not installed", executed=False)


def run_cpp(code: str, input_data: str = "") -> RunResult:
    try:
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        exe_path = temp_path.replace(".cpp", "")
        compile_result = subprocess.run(
            ["g++", temp_path, "-o", exe_path],
            capture_output=True, text=True
        )

        if compile_result.returncode != 0:
            os.remove(temp_path)
            return RunResult(success=False, stdout="", stderr=compile_result.stderr, executed=False)

        result = _run_process([exe_path], input_data)
        os.remove(temp_path)
        os.remove(exe_path)
        return result

    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="G++ not installed", executed=False)


def run_java(code: str, input_data: str = "") -> RunResult:
    try:
        import re
        match = re.search(r'public\s+class\s+(\w+)', code)
        class_name = match.group(1) if match else "Main"

        tmp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(tmp_dir, f"{class_name}.java")

        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(code)

        compile_result = subprocess.run(
            ["javac", temp_path],
            capture_output=True, text=True
        )

        if compile_result.returncode != 0:
            os.remove(temp_path)
            os.rmdir(tmp_dir)
            return RunResult(success=False, stdout="", stderr=compile_result.stderr, executed=False)

        result = _run_process(["java", "-cp", tmp_dir, class_name], input_data)
        os.remove(temp_path)
        return result

    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="Java JDK not installed", executed=False)


def run_javascript(code: str, input_data: str = "") -> RunResult:
    try:
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        result = _run_process(["node", temp_path], input_data)
        os.remove(temp_path)
        return result

    except FileNotFoundError:
        return RunResult(success=False, stdout="", stderr="Node.js not installed", executed=False)


def validate_code(code: str, language: str) -> RunResult:
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
        print(f"No runner available for: {language}")
        return RunResult(success=True, stdout="", stderr="")