.PHONY: run test lint clean docker-build docker-run

run:
	streamlit run app.py

test:
	pytest tests/ -v

lint:
	ruff check .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

docker-build:
	docker build -t voxstream .

docker-run:
	docker run -p 8501:8501 voxstream
