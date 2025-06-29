# mcp-filesystem-server
A Model Context Protocol (MCP) server for filesystem operations.

## Available Makefile Commands

- `make init` &mdash; Create a Python virtual environment and install all dependencies.
- `make install` &mdash; Install Python dependencies into the existing virtual environment.
- `make run` &mdash; Run the MCP server (ensure the virtual environment is activated).
- `make test` &mdash; Run all unit tests.

## Available Tools (Handlers)

- `open_file` &mdash; Open and read the contents of a file. Expects `{ "path": "relative/path/to/file.txt" }`.
- `list_allowed_dir` &mdash; List files and directories in the allowed root. Expects `{}`.
- `read_file` &mdash; Read a portion of a file. Expects `{ "path": "...", "offset": int, "length": int }`.
- `edit_file` &mdash; Edit or replace part/all of a file. Expects `{ "path": "...", "content": "...", "offset": int (optional) }`.
- `make_dir` &mdash; Create a new directory. Expects `{ "path": "relative/path/to/newdir" }`.

## Quick Start

1. **Initialize the environment:**
   ```sh
   make init
   ```
2. **Run the server:**
   ```sh
   make run
   ```
3. **Run tests:**
   ```sh
   make test
   ```

## Requirements
- Python 3.8+
- GNU Make

## Project Structure
- `src/mcp_server/` &mdash; Server implementation and handlers
- `tests/` &mdash; Unit tests
- `requirements.txt` &mdash; Python dependencies
- `Makefile` &mdash; Automation commands
