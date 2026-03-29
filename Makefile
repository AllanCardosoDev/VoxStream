.PHONY: install run test lint clean docker-build docker-run

## Instala as dependências do projeto
install:
	pip install -r requirements.txt

## Instala dependências de desenvolvimento (testes e linting)
install-dev:
	pip install pytest ruff

## Inicia a aplicação Streamlit
run:
	streamlit run app.py

## Executa todos os testes unitários
test:
	pytest tests/ -v --tb=short

## Verifica o estilo de código com ruff
lint:
	ruff check voxstream/ tests/ app.py

## Remove arquivos de cache e artefatos de build
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage dist build *.egg-info

## Constrói a imagem Docker
docker-build:
	docker build -t voxstream .

## Executa o container Docker
docker-run:
	docker run -p 8501:8501 voxstream

help:
	@grep -E '^## ' Makefile | sed 's/## //'
