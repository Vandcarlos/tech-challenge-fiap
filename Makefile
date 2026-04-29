.DEFAULT_GOAL := help

# --- Global vars ---
VENV = .venv

# Se estiver no GitHub Actions ou Container (CI=true), usa o Python do sistema e não exige venv
ifeq ($(CI),true)
	PYTHON   = python
	PIP      = $(PYTHON) -m pip
	VENV_DEP = # vazio
else
	BASE_PYTHON = $(shell command -v pyenv >/dev/null 2>&1 && pyenv which python || echo python3)
	BIN         = $(VENV)/bin
	PYTHON      = ./$(BIN)/python
	PIP         = $(PYTHON) -m pip
	VENV_DEP    = venv
endif

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "\033[31mErro: Variável $* é obrigatória.\033[0m Ex: make command $*=valor"; \
		exit 1; \
	fi

.PHONY: help venv

venv: ## Cria o virtualenv se não existir (apenas local)
	@echo "🐍 Configurando ambiente local..."
	@test -d $(VENV) || $(BASE_PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel

include scripts/make/*.mk

help: ## Mostra os comandos disponíveis
	@echo "\033[1;34mUso:\033[0m make <comando> [VARIÁVEL=valor]"
	@echo ""
	@echo "\033[1;33mComandos:\033[0m"
	@grep -Eh '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[1;33mParâmetros:\033[0m"
	@grep -Eh '^[a-zA-Z_-]+ \?=.*?##@ .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = " \\?=.*?##@ "}; {printf "  \033[32m%-25s\033[0m %s\n", $$1, $$2}'
