import argparse #handle CLI argument
import subprocess #talk to OLLama
import sys #read stdin
from pathlib import Path #Safe file handling

from agent.language_detector import detect_language # for early language detection
from agent.error_classifier import classify_error #for the early error classficattiono

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
    
        

def build_prompt(code: str, language: str, error_type: str)-> str :
     template = Path("prompts/debugger.txt").read_text(encoding="utf-8")
     structured_context = f"""
     Detected Language: {language}
     Pre-analysis Result: {error_type}

     CODE:
     {code}
     """
     return template.replace("{code}", structured_context)


def call_ai(prompt: str)-> str:
     result = subprocess.run(
          ["ollama", "run", "deepseek-coder:6.7b"],  

          input=prompt,
          text= True, #Without this, Python would return raw byte data.
          capture_output=True,
          encoding="utf-8" #Decode output using UTF-8 without this system will suffer from a bug
            )
     
     return result.stdout.strip() 

def extract_fixed_code(ai_output: str)->str|None:
     '''Extract the fixed code section from AI output'''
    
     if "FIXED CODE:" not in ai_output:
          return None
     parts = ai_output.split("FIXED CODE:")

     if len(parts)<2:
          return None
     
     fixed_section =parts[1].strip()#This takes only the fixed code section.
     if fixed_section.startswith("```"):  #Markdown markers:
          fixed_section=fixed_section.split("```",1)[1] #This removes the first markdown marker.
          fixed_section=fixed_section.split("```",1)[0] #This removes the last markdown marker.after this we will only have the clean code
          return fixed_section.strip() #This is the final code which is going to be written on the file by agent
          
def apply_fix(file_path: str, fixed_code: str):
     '''
     Docstring for apply_fix\
     Safely apply fix:
     create backup 
     overwrite original file
    
     '''
     original = Path(file_path) #Path object is safer than plain string.
    
     backup = original.with_suffix(original.suffix + ".bak") #test.py → test.py.bak Now backup file path is ready
     
     backup.write_text(original.read_text(encoding="utf-8"),encoding="utf-8") #This is very important | this creates backup file.

     original.write_text(fixed_code, encoding="utf-8") #This overwrited original file with fixed code

     print(f"Fix applied successfully")

     print(f"Backup created at :{backup}") # thsi shows backup file location
def main():
     args=get_arguments()
     code = read_code(args)
     language = detect_language(code, args.file)
     error_type = classify_error(code)

     print(f" Detected Language: {language}")
     print(f"Pre-analysis:{error_type}")
     print("Debuggin......\n")

     prompt= build_prompt(code,language,error_type)
     output= call_ai(prompt)

     print("Result:\n")
     print(output)

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