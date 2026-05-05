.PHONY: train


TRAIN_DATA_SOURCE_PATH ?= './data/silver'##@ [train] Opcional: Caminho de origem dos dados, por padrão './data/silver'.
TRAIN_DATA_TARGET_PATH ?= './data/gold'##@ [train] Opcional: Caminho de destino dos dados gerados, por padrão './data/gold'.
TRAIN_ARTIFACTS_TARGET_PATH ?= './models/train'##@ [train] Opcional: Caminho de destino dos artefados gerados, por padrão './models/train'.
TRAIN_YEAR_MONTH ?= ##@ [train] Opcional: Partição YYYYMM. Se não fornecida, usa a ultima partição.
train: ## Faz o treinamento dos dados de uma determianda partição (mês)
	PYTHONPATH=. $(PYTHON) -m src.cli.train \
		--SOURCE_PATH $(TRAIN_DATA_SOURCE_PATH) \
		--TARGET_PATH $(TRAIN_DATA_TARGET_PATH) \
		--ARTIFACTS_PATH $(TRAIN_ARTIFACTS_TARGET_PATH) \
		$(if $(TRAIN_YEAR_MONTH),--YEAR_MONTH $(TRAIN_YEAR_MONTH),) \
