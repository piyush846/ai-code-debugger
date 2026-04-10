import argparse
import sys
from aidbg.orchestrator import debug


def get_arguments():
    parser = argparse.ArgumentParser(description="aidbg — AI Code Debugger (local, offline)")
    parser.add_argument("file", nargs="?", help="Path to source file")
    parser.add_argument("--fix", action="store_true", help="Automatically apply fix (with backup)")
    return parser.parse_args()


def main():
    args = get_arguments()

    if not args.file:
        print("Usage: aidbg <file> [--fix]")
        sys.exit(1)

    result = debug(args.file, max_attempts=4)

    status = result.get("status")

    if status == "ok":
        print("\nNo errors found. Code is valid.")

    elif status == "fixed":
        print(f"\nFixed in {result['attempts']} attempt(s).")
        print(f"\nExplanation: {result['explanation']}")

    elif status == "failed":
        print(f"\nCould not fix the code.")
        print(f"Last compiler error:\n{result.get('last_error', '')}")

    elif status == "error":
        print(f"\nError: {result.get('message')}")
        sys.exit(1)


if __name__ == "__main__":
    main()