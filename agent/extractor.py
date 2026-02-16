def extract_fixed_code(ai_output: str) -> str | None:
    """
    Extract the fixed code section from AI output.
    Supports markdown and plain text.
    Removes markdown language labels like python, cpp, c++, java, js.
    """

    if "FIXED CODE:" not in ai_output:
        return None

    # Step 1: get everything after FIXED CODE:
    fixed_section = ai_output.split("FIXED CODE:", 1)[1].strip()


    # Step 2: handle markdown code blocks
    if "```" in fixed_section:

        parts = fixed_section.split("```")

        if len(parts) >= 2:

            code_block = parts[1].strip()

            lines = code_block.splitlines()

            # Step 3: remove language label line
            if lines:

                first_line = lines[0].strip().lower()

                language_labels = [
                    "python",
                    "cpp",
                    "c++",
                    "c",
                    "java",
                    "javascript",
                    "js"
                ]

                if first_line in language_labels:
                    lines = lines[1:]

            code_block = "\n".join(lines)

            return code_block.strip()


    # Step 4: fallback plain text
    fixed_section = fixed_section.strip()

    return fixed_section if fixed_section else None
