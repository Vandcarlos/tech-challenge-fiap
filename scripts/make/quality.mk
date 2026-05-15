RUFF 	 = $(BIN)/ruff
MYPY 	 = $(BIN)/mypy

ifeq ($(CI),true)
	PYTEST   = pytest
else
	PYTEST   = $(BIN)/pytest
endif

.PHONY: lint test

lint: ## Roda ruff para verificar a qualidade do código (mypy desabilitado temporariamente para performance)
	@echo "🔍 Rodando Linter..."
	$(RUFF) check src tests
	@echo "🎨 Rodando Formatter Check..."
	$(RUFF) format --check src tests
	@echo "✅ Lint concluído (mypy desabilitado para performance)"

type-check: ## Roda apenas mypy para verificação de tipos (mais lento)
	@echo "🧪 Rodando Type Check..."
	MYPYPATH=typings $(MYPY) src

MIN_COVERAGE ?= 75 ##@ [test] Opcional: Cobertura mínima para testes (padrão: 75)
VERBOSE ?= false ##@ [test] Opcional: Se true, executa os testes em modo verbose (padrão: false)
test: ## Roda os testes usando pytest e verifica se a cobertura é maior ou igual a MIN_COVERAGE
	PYTHONPATH=. $(PYTEST) --cov=src --cov-report=xml --cov-fail-under=$(MIN_COVERAGE) \
		$(if $(filter true,$(VERBOSE)),-vv,)
