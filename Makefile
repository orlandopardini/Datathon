.PHONY: train api test dashboard

train:
	python -m src.train --data-path "$(DATA_PATH)" --sheet "$(SHEET)"

api:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	pytest --cov=src --cov=app --cov-report=term-missing --cov-fail-under=80

dashboard:
	streamlit run monitoring/dashboard.py
