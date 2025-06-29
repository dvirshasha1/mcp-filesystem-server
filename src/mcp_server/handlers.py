import os

# Handlers for MCP methods (open, read, edit)

def get_allowed_root():
    """Get the allowed root directory from env or default to cwd."""
    return os.environ.get("MCP_ALLOWED_ROOT") or os.getcwd()

def open_file(request, allowed_root=None):
    """
    Handler to open and read the contents of a file.
    Expects: { "path": "relative/path/to/file.txt" }
    Returns: { "content": "..." } or { "error": "..." }
    """
    path = request.get("path")
    if not path:
        return {"error": "Missing 'path' in request."}
    # Restrict to a safe directory (allowed root)
    safe_root = allowed_root or get_allowed_root()
    abs_path = os.path.abspath(os.path.join(safe_root, path))
    if not abs_path.startswith(os.path.abspath(safe_root)):
        return {"error": "Access denied."}
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

def list_allowed_dir(request, allowed_root=None):
    """
    Handler to list the contents of the allowed directory.
    Expects: {}
    Returns: { "files": ["file1.txt", "subdir/", ...] } or { "error": "..." }
    Optionally accepts allowed_root as a parameter for testing or server config.
    """
    root = allowed_root or os.environ.get("MCP_ALLOWED_ROOT") or os.getcwd()
    try:
        entries = os.listdir(root)
        # Mark directories with a trailing slash
        files = [e + "/" if os.path.isdir(os.path.join(root, e)) else e for e in entries]
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

def read_file(request, allowed_root=None):
    """
    Handler to read a portion of a file.
    Expects: { "path": "...", "offset": int, "length": int }
    Returns: { "content": "..." } or { "error": "..." }
    """
    path = request.get("path")
    offset = request.get("offset", 0)
    length = request.get("length")
    if not path or length is None:
        return {"error": "Missing 'path' or 'length' in request."}
    safe_root = allowed_root or get_allowed_root()
    abs_path = os.path.abspath(os.path.join(safe_root, path))
    if not abs_path.startswith(os.path.abspath(safe_root)):
        return {"error": "Access denied."}
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            f.seek(offset)
            content = f.read(length)
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

def edit_file(request, allowed_root=None):
    """
    Handler to edit/replace part or all of a file.
    Expects: { "path": "...", "content": "...", "offset": int (optional) }
    Returns: { "success": true } or { "error": "..." }
    """
    path = request.get("path")
    content = request.get("content")
    offset = request.get("offset", 0)
    if not path or content is None:
        return {"error": "Missing 'path' or 'content' in request."}
    safe_root = allowed_root or get_allowed_root()
    abs_path = os.path.abspath(os.path.join(safe_root, path))
    if not abs_path.startswith(os.path.abspath(safe_root)):
        return {"error": "Access denied."}
    try:
        # If offset is 0, overwrite the file. Otherwise, edit at offset.
        if offset == 0:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            with open(abs_path, "r+b") as f:
                f.seek(offset)
                f.write(content.encode("utf-8"))
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def make_dir(request, allowed_root=None):
    """
    Handler to create a new directory.
    Expects: { "path": "relative/path/to/newdir" }
    Returns: { "success": True } or { "error": "..." }
    """
    path = request.get("path")
    if not path:
        return {"error": "Missing 'path' in request."}
    safe_root = allowed_root or get_allowed_root()
    abs_path = os.path.abspath(os.path.join(safe_root, path))
    if not abs_path.startswith(os.path.abspath(safe_root)):
        return {"error": "Access denied."}
    try:
        os.makedirs(abs_path, exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

