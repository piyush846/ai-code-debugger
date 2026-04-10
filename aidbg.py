import argparse #handle CLI argument
import subprocess #talk to OLLama
import sys #read stdin
import os
import shutil
from pathlib import Path #Safe file handling
from agent.validator import validate_python_syntax
from agent.language_detector import detect_language # for early language detection
from agent.error_classifier import classify_error #for the early error classficattiono
from agent.extractor import extract_fixed_code
from agent.retry import retry_fix
from agent.ai_client import call_ai
from agent.fixer import apply_fix
from agent.compiler_validator import validate_code

def get_arguments():
    parser =argparse.ArgumentParser(
        description="AI Code Debugger(Free,Local)"
    )

    
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to Code file"

    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read code from standard input"
    )
    parser.add_argument(
         "--fix",
         action="store_true",
         help="Automatically apply the suggested fix(safe mode with backup)"
    )

    return parser.parse_args() #Reads terminal input Validates arguments Converts them into object Returns structured result


def  read_code(args):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        path = Path(args.file)

        if not path.exists():
               
               print("File not Found")
               sys.exit(1) #  1 menas failur or error code
        return path.read_text(encoding ="utf-8")
    print ("provide a file or use --stdin")
    sys.exit(1)
    
        

def build_prompt(code: str, language: str, error_type: str) -> str:
    template = Path("prompts/debugger.txt").read_text(encoding="utf-8")
    return (template
            .replace("{code}", code)
            .replace("{language}", language)
            .replace("{error_type}", error_type))


def main():
     args=get_arguments()
     code = read_code(args)
     print(f"File being processed : {args.file}")
     language = detect_language(code, args.file)
     error_type = classify_error(code)

     print(f" Detected Language: {language}")
     print(f"Pre-analysis:{error_type}")
     print("Debuggin......\n")

     prompt= build_prompt(code,language,error_type)
     output= call_ai(prompt)

     print("Result:\n")
     print(output)

     if args.fix and args.file:
          print("\n Applying fix in safe mode...")

          fixed_code= retry_fix(call_ai,
                                build_prompt,
                                code,
                                language,
                                error_type,
                                args.file,
                                max_attempts=4
                                )
          if fixed_code is None:
               print(" NO error found or Failed to generate valid after multiple attempts")
               return

          is_valid = validate_code(fixed_code,language)

          if not is_valid:
               print("fix failed compiler validatioin")
               print("Original file preserved")
               return
          apply_fix(args.file, fixed_code)
          
          print("Syntax validation passed. Fix applied successfully")
if __name__=="__main__":
     main()
'''strip() removes extra: Spaces New lines It ccleans the output before returning '''

    
'''Your code builds a:p

Command-Line AI Debugger Tool
that reads code → sends it to a local AI model → prints debugging output.

It is:

 CLI-based

 IDE-independent

 Local (offline AI)

 Modular
 
  User (Terminal)
        ↓
get_arguments()
        ↓
read_code()
        ↓
build_prompt()
        ↓
call_ai()
        ↓
print result 

read_code function works for :
If stdin → read from stdin
Else if file → check file exists → read file
Else → show error and exit
Decides where the code comes from, reads it safely, and returns it.

build prompt:
this function build a very  structured analysis
Detected Language: Python
Pre-analysis Result: Possible Python syntax error

CODE:
def add(a,b)
    return a+b
    
    Simple Summary of call_ai()

This function:

Takes prompt
   ↓
Runs Ollama
   ↓
Sends prompt to model
   ↓
Receives AI answer
   ↓
Returns cleaned result

extract_fixed_code():
This is very important function


# Why This Function Is Critical

Without this function:

Your program cannot safely extract fixed code.

AI output contains:

- explanation
- markdown
- extra text

This function extracts only usable code.

---

# Visual Flow

AI Output
↓
Find "FIXED CODE:"
↓
Extract section
↓
Remove markdown
↓
Return clean code

apply fix:
this is the function which enable agentic behaviour

Original file → read content
             ↓
Create backup file
             ↓
Write fixed code to original file
             ↓
Show success message
Why Backup Is Critical
Without backup:

If AI makes mistake → original file lost.

With backup:

You can restore original anytime.

Professional tools ALWAYS create backups.
'''