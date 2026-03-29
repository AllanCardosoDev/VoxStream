.PHONY: run test test-cov install clean lint help

## Executa a aplicação Streamlit
run:
	streamlit run app.py

## Instala as dependências
install:
	pip install -r requirements.txt

## Instala as dependências de desenvolvimento
install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov

## Executa os testes unitários
test:
	pytest tests/ -v

## Executa os testes com relatório de cobertura
test-cov:
	pytest tests/ -v --cov=voxstream --cov-report=term-missing --cov-report=html

## Limpa artefatos de build e cache
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage dist build *.egg-info

## Exibe esta ajuda
help:
	@echo ""
	@echo "Comandos disponíveis:"
	@grep -E '^## ' Makefile | sed 's/## /  /'
	@echo ""
	@grep -E '^[a-zA-Z_-]+:' Makefile | grep -v '.PHONY' | sed 's/:.*//' | awk '{printf "    make %-15s\n", $$1}'
	@echo ""
