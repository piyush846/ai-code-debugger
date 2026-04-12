import os
import shutil
import subprocess
import requests
from aidbg.config import MODEL, OLLAMA_HOST, OLLAMA_TIMEOUT


def call_ai(prompt: str, system: str = "") -> str:
    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    # Try HTTP API first (works inside Docker)
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": MODEL,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=OLLAMA_TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            print(f"[ollama] HTTP error {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[ollama] Cannot reach {OLLAMA_HOST}, trying CLI...")
    except requests.exceptions.Timeout:
        print(f"[ollama] Timed out after {OLLAMA_TIMEOUT}s")
        return ""
    except Exception as e:
        print(f"[ollama] HTTP failed: {e}, trying CLI...")

    # Fallback to CLI (works locally)
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        win_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
        if os.path.isfile(win_path):
            ollama_path = win_path

    if not ollama_path:
        print("ERROR: Ollama not found.")
        return ""

    print(f"[ollama] Using model: {MODEL}")

    try:
        result = subprocess.run(
            [ollama_path, "run", MODEL],
            input=full_prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=OLLAMA_TIMEOUT
        )
        if result.returncode != 0:
            print("ERROR: Ollama CLI failed.")
            return ""
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print(f"ERROR: Timed out after {OLLAMA_TIMEOUT}s.")
        return ""
    except KeyboardInterrupt:
        print("\n[ollama] Interrupted.")
        return ""
    except Exception as e:
        print("CRITICAL ERROR:", str(e))
        return ""