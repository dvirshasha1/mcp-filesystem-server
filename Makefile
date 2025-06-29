VENV=.venv

init:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -U pip && pip install -r requirements.txt

install:
	. $(VENV)/bin/activate && pip install -r requirements.txt

run:
	. $(VENV)/bin/activate && python src/mcp_server/main.py

test:
	PYTHONPATH=src .venv/bin/pytest
