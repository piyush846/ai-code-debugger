from pathlib import Path #help us to work with file name safely

def detect_language(code:str, filename: str |None = None) ->str:
    if filename:
        suffix=Path(filename).suffix.lower()
        if suffix ==".py":
            return "Python"
        if suffix == ".js":
            return "Javascript"
        if suffix in[".cpp",".cc",".ccx"]:
            return "C++"
        if suffix ==".c":
            return "C"
        if suffix == ".java":
            return "Java"
    
    code_lower=code.lower()
    if "def" in code_lower:
        return "Python"
    if "#include" in code_lower:
        return "C/C++"
    if "public static void main" in code_lower:
        return "Java"
    if "console.log" in code_lower:
        return "Javascript"
    
    return "Unknown"

'''
Do we have filename?
    Yes → Check extension → Return language
    No  → Check code text → Return language
If nothing matches → Return Unknown
'''