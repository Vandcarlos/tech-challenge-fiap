RUFF 	 = $(BIN)/ruff
MYPY 	 = $(BIN)/mypy

ifeq ($(CI),true)
	PYTEST   = pytest
else
	PYTEST   = $(BIN)/pytest
endif

PYTHONPATH=. $(PYTEST) --cov=src --cov-report=xml --cov-fail-under=$(MIN_COVERAGE)
.PHONY: lint test

lint: ## Roda ruff e mypy para verificar a qualidade do código
	@echo "🔍 Rodando Linter..."
	$(RUFF) check src tests
	@echo "🎨 Rodando Formatter Check..."
	$(RUFF) format --check src tests
	@echo "🧪 Rodando Type Check..."
	MYPYPATH=typings $(MYPY) src

MIN_COVERAGE ?= 90##@ [test] Opcional: Cobertura mínima para testes (padrão: 90)
VERBOSE ?= false ##@ [test] Opcional: Se true, executa os testes em modo verbose (padrão: false)
test: ## Roda os testes usando pytest e verifica se a cobertura é maior ou igual a MIN_COVERAGE
	PYTHONPATH=. $(PYTEST) --cov=src --cov-report=xml --cov-fail-under=$(MIN_COVERAGE) \
		$(if $(filter true,$(VERBOSE)),-vv,)
