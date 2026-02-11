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

    return parser.parse_args() #Reads terminal input Validates arguments Converts them into object Returns structured result


def  read_code(args):
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        path = Path(args.file)

        if not path.exists():
               
               Print("File not Found")
               sys.exit(1) #  1 menas failur or error code
        return path.read_text(encoding ="utf-8")
    print ("provide a file or use --stdin")
    sys.exit(1)
    
        

    
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
'''