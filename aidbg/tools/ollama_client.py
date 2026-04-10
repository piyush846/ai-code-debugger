import os
import shutil
import subprocess


def call_ai(prompt: str, system: str = "") -> str:
    """
    Call Ollama model with optional system prompt.
    Each agent passes its own system prompt to specialise behaviour.
    """
    ollama_path = shutil.which("ollama")

    if not ollama_path:
        win_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
        if os.path.isfile(win_path):
            ollama_path = win_path

    if not ollama_path:
        print("ERROR: Ollama not found.")
        return ""

    model = os.environ.get("AIDBG_MODEL", "qwen2.5-coder:3b")
    print(f"Using model: {model}")

    # Inject system prompt into user prompt since ollama CLI doesn't
    # support --system flag in all versions
    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    try:
        result = subprocess.run(
            [ollama_path, "run", model],
            input=full_prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=300
        )

        if result.returncode != 0:
            print("ERROR: Ollama execution failed.")
            if result.stderr:
                print("stderr:", result.stderr)
            return ""

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print("ERROR: Ollama timed out.")
        return ""

    except Exception as e:
        print("CRITICAL ERROR:", str(e))
        return ""