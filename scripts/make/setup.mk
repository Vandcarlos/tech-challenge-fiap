.PHONY: setup-notebooks setup-ingest setup-tests  setup

setup-notebooks: venv ## Instala as dependências necessárias para rodar os notebooks
	@echo "Installing notebook dependencies..."; \
	$(PIP) install -e ".[notebooks]"

setup-ingest: venv ## Instala as dependências necessárias para rodar os scripts de ingestão
	@echo "Installing ingest dependencies"; \
	$(PIP) install -e ".[ingest]"

setup-tests: venv ## Instala as dependências necessárias para rodar os testes
	@echo "Installing test dependencies..."; \
	$(PIP) install -e ".[tests,ingest]"

setup: venv ## Instala todas as dependências do projeto
	@echo "Installing project dependencies..."; \
	$(PIP) install -e .[dev,tests,ingest,notebooks]
