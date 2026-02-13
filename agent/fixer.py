from pathlib import Path
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

     print(f"Backup created at :{backup}") # this shows backup file location

