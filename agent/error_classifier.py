def classify_error(code:str)->str:
    code_lower = code.lower()

    if "def" in code_lower and ":" not in code_lower:
        return "Possible Python syntax error(missing colon)"
    
    if "while(true)" in code_lower:
        return "Possible infinite Loop"
    
    if "int" in code_lower and ";" not in code_lower:
        return "Possible missing semicolon"
    
    return "Unknown or Logical error"
    