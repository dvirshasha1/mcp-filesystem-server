# Unit tests for MCP handlers

import os
import tempfile
import shutil
import pytest
from mcp_server import handlers

def setup_temp_dir(files):
    temp_dir = tempfile.mkdtemp()
    for name, content in files.items():
        file_path = os.path.join(temp_dir, name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    return temp_dir

def test_open_file_reads_content():
    temp_dir = setup_temp_dir({"foo.txt": "hello world"})
    req = {"path": "foo.txt"}
    resp = handlers.open_file(req, allowed_root=temp_dir)
    assert resp["content"] == "hello world"
    shutil.rmtree(temp_dir)

def test_open_file_denies_outside():
    temp_dir = setup_temp_dir({"foo.txt": "hi"})
    req = {"path": "../foo.txt"}
    resp = handlers.open_file(req, allowed_root=temp_dir)
    assert "error" in resp
    shutil.rmtree(temp_dir)

def test_list_allowed_dir_lists_files():
    temp_dir = setup_temp_dir({"a.txt": "1", "b.txt": "2"})
    req = {}
    resp = handlers.list_allowed_dir(req, allowed_root=temp_dir)
    assert set(resp["files"]) >= {"a.txt", "b.txt"}
    shutil.rmtree(temp_dir)

def test_read_file_reads_slice():
    temp_dir = setup_temp_dir({"foo.txt": "abcdefg"})
    req = {"path": "foo.txt", "offset": 2, "length": 3}
    resp = handlers.read_file(req, allowed_root=temp_dir)
    assert resp["content"] == "cde"
    shutil.rmtree(temp_dir)

def test_edit_file_overwrites():
    temp_dir = setup_temp_dir({"foo.txt": "old content"})
    req = {"path": "foo.txt", "content": "new content"}
    resp = handlers.edit_file(req, allowed_root=temp_dir)
    assert resp["success"]
    with open(os.path.join(temp_dir, "foo.txt")) as f:
        assert f.read() == "new content"
    shutil.rmtree(temp_dir)

def test_edit_file_at_offset():
    temp_dir = setup_temp_dir({"foo.txt": "abcdefg"})
    req = {"path": "foo.txt", "content": "ZZZ", "offset": 2}
    resp = handlers.edit_file(req, allowed_root=temp_dir)
    assert resp["success"]
    with open(os.path.join(temp_dir, "foo.txt")) as f:
        assert f.read() == "abZZZfg"
    shutil.rmtree(temp_dir)

def test_make_dir_creates_directory():
    temp_dir = setup_temp_dir({})
    req = {"path": "newdir/subdir"}
    resp = handlers.make_dir(req, allowed_root=temp_dir)
    assert resp["success"]
    assert os.path.isdir(os.path.join(temp_dir, "newdir", "subdir"))
    shutil.rmtree(temp_dir)
