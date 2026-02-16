import subprocess
import tempfile #this creates temporary file for compiler validation because compiler only accepts file
from pathlib import Path
import os

def validate_python(code:str)->bool:
    try:
        compile(code,"<string>","exec")
        return True
    except SyntaxError:
        return False


def validate_javascript(code:str)->bool:
    try:
        result =subprocess.run(
            ["node","--check"],
            input=code,
            text=True,
            capture_output=True
        )
        return result.returncode == 0
    
    except FileNotFoundError:
        print("Validator error : Node.js not installed")
        return False

def validate_c(code: str)->bool:
    try:
        with tempfile.NamedTemporaryFile(suffix=".c",delete=False,mode="w",encoding="utf-8") as f:
            f.write(code)
            temp_path =f.name

        result = subprocess.run(
            ["gcc", "-fsyntax-only",temp_path],
            capture_output=True,
            text=True,
        ) 
        os.remove(temp_path)

        return result.returncode == 0
    
    except FileNotFoundError:
        print("validator Error: GCC not installed")
        return False
    
def validate_cpp(code:str)->bool:
    try:
        with tempfile.NamedTemporaryFile(suffix=".cpp",delete=False, mode="w" ,encoding ="utf-8") as f:
            f.write(code)
            temp_path =f.name

        result = subprocess.run(
            ["g++", "-fsyntax-only",temp_path],
            capture_output=True,
            text=True
        )
        print("DEBUG g++ return code:", result.returncode)
        print("DEBUG g++ stderr:", result.stderr)
        os.remove(temp_path)

        return result.returncode == 0
    
    except FileNotFoundError:
        print("validor error:G++ not installed")
        return False
    

def validate_java(code:str)->bool:
    try:
        with tempfile.NamedTemporaryFile(suffix=".java", delete=False, mode="w", encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name


        result = subprocess.run(
            ["javac",temp_path],
            capture_output=True,
            text = True

        )
        os.remove(temp_path)
        return result.returncode ==0
    
    except FileNotFoundError:
        print("Validator error:Java JDK not installed")
        return False
    

def validate_code(code:str, language:str)->bool:

    language=language.lower()

    if language == "python":
        return validate_python(code)
    
    elif language=="javascript":
        return validate_javascript(code)
    
    elif language=="c":
        return validate_c(code)
    
    elif language =="c++":
        return validate_cpp(code)
    
    elif language == "java":
        return validate_java(code)
    
    else:
        print(f"No Validator available for{language}")
        return True


        
