from agent.compiler_validator import validate_code
from agent.extractor import extract_fixed_code

def retry_fix(call_ai, build_prompt, code, language,error_type,filename ,max_attempts=4):
    attempt =1
    while attempt<= max_attempts:
        print(f"attempt {attempt} of {max_attempts}")

        prompt=build_prompt(code,language, error_type)

        output = call_ai(prompt)
        print("\nDebug : RAW AI OUTPUT \n")
        print( output)
        print("\nDebug end\n")

        fixed_code= extract_fixed_code(output)

        if not fixed_code:
            print("Could not extract fix from AI response")
            attempt += 1
            continue #skip ramaining steps go to next attempt
        valid = validate_code(fixed_code,language)

        if valid:
            print("valid fix found")
            return fixed_code
        print("Invalid fix: compiler validtion failed")

        code =fixed_code # It upadates input code for next attempt Instead of retrying original broken code, agent retries improved version.

        attempt += 1
    return None    


'''
roken code:

def add(a,b)
    return a+b


Agent flow:

Attempt 1
LLM fix invalid
retry

Attempt 2
LLM fix valid
return fixed_code

Why retry loop makes this a real agent

Without retry:

LLM fails → agent fails


With retry:

LLM fails → agent retries → succeeds


Agent becomes persistent.
'''