import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "aidbg.mcp.server"],
        cwd="C:\\Users\\91968\\Desktop\\Ai_codedebugger"
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

asyncio.run(main())