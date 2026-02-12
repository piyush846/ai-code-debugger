def validate_python_syntax(code: str, filename: str ="<string>")-> tuple[bool,str | None]:
    try:
        compile(code, filename, "exec") #this tell python check if this code is valid syntax
        return True, None
    except SyntaxError as e:
        return False, f"{e.msg} at line {e.lineno}" # returns expected ':' at line 1"
    except Exception as e: # it catches any unexpected error
        return False ,str(e)
