from fastmcp.server.server import FastMCP
import handlers
from fastmcp.tools.tool import Tool

server = FastMCP(
    name="MCP Server",
    instructions="Custom MCP server with file and directory handlers.",
    tools=[
        Tool.from_function(handlers.open_file, name="open_file", description="Open and read a file"),
        Tool.from_function(handlers.read_file, name="read_file", description="Read a portion of a file"),
        Tool.from_function(handlers.edit_file, name="edit_file", description="Edit or replace part or all of a file"),
        Tool.from_function(handlers.list_allowed_dir, name="list_allowed_dir", description="List files and directories"),
        Tool.from_function(handlers.make_dir, name="make_dir", description="Create a new directory"),
    ]
)

# Main entrypoint for the MCP server
if __name__ == "__main__":
    server.run(transport="stdio")
