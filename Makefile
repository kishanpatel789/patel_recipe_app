SHELL := /bin/bash

VENV_NAME = venv
ACTIVATE_SCRIPT = source ./$(VENV_NAME)/bin/activate

venv:
	$(ACTIVATE_SCRIPT)

dev_api: venv
	uvicorn api.main:app --port 8000 --reload

dev_ui: 
	source venv/bin/activate && python ui/wsgi.py

.PHONY: venv dev_api dev_ui 