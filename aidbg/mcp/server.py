import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from aidbg.orchestrator import debug


app = Server("aidbg")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="debug_file",
            description="Debug a source file using AI agents. Analyses, fixes, and explains the bug.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Absolute path to the source file to debug"
                    },
                    "max_attempts": {
                        "type": "integer",
                        "description": "Max fix attempts (default 4)",
                        "default": 4
                    }
                },
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="analyse_file",
            description="Only analyse a source file — detect language and classify error type. Does not fix.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Absolute path to the source file"
                    }
                },
                "required": ["filepath"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "debug_file":
        filepath = arguments.get("filepath", "")
        max_attempts = arguments.get("max_attempts", 4)

        result = debug(filepath, max_attempts=max_attempts)

        status = result.get("status")

        if status == "ok":
            text = "No errors found. Code is already valid."

        elif status == "fixed":
            text = (
                f"Fixed in {result['attempts']} attempt(s).\n\n"
                f"Explanation: {result['explanation']}"
            )

        elif status == "failed":
            text = (
                f"Could not fix after {max_attempts} attempts.\n"
                f"Last compiler error:\n{result.get('last_error', 'unknown')}"
            )

        else:
            text = f"Error: {result.get('message', 'unknown error')}"

        return [types.TextContent(type="text", text=text)]

    elif name == "analyse_file":
        from pathlib import Path
        from aidbg.agents.analyser import analyse

        filepath = arguments.get("filepath", "")
        path = Path(filepath).resolve()

        if not path.exists():
            return [types.TextContent(type="text", text=f"File not found: {filepath}")]

        code = path.read_text(encoding="utf-8")
        result = analyse(code, filepath)

        text = (
            f"Language: {result['language']}\n"
            f"Pre-analysis: {result['error_type']}"
        )
        return [types.TextContent(type="text", text=text)]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())