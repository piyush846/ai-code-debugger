import argparse #handle CLI argument
import subprocess #talk to OLLama
import sys #read stdin
from pathlib import Path #Safe file handling

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
        action="store-true",
        help="Read code from standard input"
    )

    return parser.parse_args() #Reads terminal input Validates arguments Converts them into object Returns structured result
'''Your code builds a:

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
print result '''