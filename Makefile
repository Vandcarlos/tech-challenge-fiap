.DEFAULT_GOAL := help

# --- Global vars ---
VENV     = .venv
BIN      = $(VENV)/bin
PYENV_PY  = $(shell pyenv which python)
PYTHON   = ./$(BIN)/python
PIP      = $(PYTHON) -m pip

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "\033[31mErro: Variável $* é obrigatória.\033[0m Ex: make command $*=valor"; \
		exit 1; \
	fi

.PHONY: help venv

venv: ## Cria o virtualenv se não existir
	@echo "🐍 Usando Python do pyenv: $(shell pyenv version-name)"
	@test -d $(VENV) || $(PYENV_PY) -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel

include scripts/make/*.mk

.PHONY: help
help: ## Mostra os comandos disponíveis
	@echo "\033[1;34mUso:\033[0m make <comando> [VARIÁVEL=valor]"
	@echo ""
	@echo "\033[1;33mComandos:\033[0m"
	@grep -Eh '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[1;33mParâmetros:\033[0m"
	@grep -Eh '^[a-zA-Z_-]+ \?=.*?##@ .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = " \\?=.*?##@ "}; {printf "  \033[32m%-25s\033[0m %s\n", $$1, $$2}'
