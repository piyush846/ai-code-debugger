import os
import subprocess
def call_ai(prompt: str) -> str:
    """
    Call Ollama model safely using absolute path.
    """

    # HARD-SET absolute path (this is correct on your system)
    ollama_path = r"C:\Users\91968\AppData\Local\Programs\Ollama\ollama.exe"

    # Step 1: Verify executable exists
    if not os.path.isfile(ollama_path):
        print("CRITICAL ERROR: Ollama executable not found at:")
        print(ollama_path)
        return ""

    try:

        # Step 2: Run Ollama model
        result = subprocess.run(
            [ollama_path, "run", "deepseek-coder:6.7b"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=120
        )

        # Step 3: Debug info
        print("DEBUG return code:", result.returncode)
        print("DEBUG stderr:", result.stderr)

        # Step 4: Check failure
        if result.returncode != 0:
            print("ERROR: Ollama execution failed")
            return ""

        # Step 5: Return clean output
        return result.stdout.strip()

    except Exception as e:
        print("CRITICAL ERROR:", str(e))
        return ""
     