dev_api: 
	uvicorn api.main:app --port 8000 --reload

dev_ui: 
	source venv/bin/activate && python ui/wsgi.py

.PHONY: dev_api dev_ui 