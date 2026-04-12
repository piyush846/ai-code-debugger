"""
aidbg configuration.

Change DEFAULT_MODEL based on your RAM:
  4GB  → qwen2.5-coder:1.5b
  8GB  → qwen2.5-coder:3b 
  16GB → qwen2.5-coder:7b / deepseek-coder:6.7b
  32GB → deepseek-coder:33b
  first  you have to pull the model by:
  ollama pull your_model_name
  and then you can change default model and use it
  
"""

import os

# --- Change this line to switch models ---
DEFAULT_MODEL = "qwen2.5-coder:3b"
# -----------------------------------------

MODEL = os.environ.get("AIDBG_MODEL", DEFAULT_MODEL)
OLLAMA_HOST = os.environ.get("AIDBG_OLLAMA_HOST", "http://localhost:11434")
MAX_ATTEMPTS = int(os.environ.get("AIDBG_MAX_ATTEMPTS", "4"))
OLLAMA_TIMEOUT = int(os.environ.get("AIDBG_TIMEOUT", "300"))