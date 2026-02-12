def extract_fixed_code(ai_output: str)->str|None:
     '''Extract the fixed code section from AI output
     works with markdown adn plain text'''
    
     if "FIXED CODE:" not in ai_output:
          return None
     fixed_section = ai_output.split("FIXED CODE:",1)[1]
     fixed_section = str(fixed_section)


     if "```"in fixed_section:
          parts = fixed_section.split("```")
          if len(parts)>=2:
               fixed_section=parts[1]

               lines = fixed_section.splitlines()
               if len(lines)>0 and lines[0].lower().strip() =="python":
                    fixed_section="\n".join(lines[1:])
              
     fixed_section = fixed_section.strip()

     return fixed_section if fixed_section else None
