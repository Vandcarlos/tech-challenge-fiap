.PHONY: setup-notebooks setup-ingest setup-tests  setup

setup-notebooks: $(VENV_DEP) ## Instala as dependências necessárias para rodar os notebooks
	@echo "Installing notebook dependencies..."; \
	$(PIP) install -e ".[notebooks]"

setup-ingest: $(VENV_DEP) ## Instala as dependências necessárias para rodar os scripts de ingestão
	@echo "Installing ingest dependencies"; \
	$(PIP) install -e ".[ingest]"

setup-tests: $(VENV_DEP) ## Instala as dependências necessárias para rodar os testes
	@echo "Installing test dependencies..."; \
	$(PIP) install -e ".[tests,ingest]"

setup: $(VENV_DEP) ## Instala todas as dependências do projeto
	@echo "Installing project dependencies..."; \
	$(PIP) install -e .[dev,tests,ingest,notebooks]
