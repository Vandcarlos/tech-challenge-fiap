.PHONY: ingest ingest-extract ingest-fake


INGEST_DATA_SOURCE_PATH ?= './data/bronze'##@ [ingest] Opcional: Caminho de origem dos dados, por padrão './data/bronze'.
INGEST_DATA_TARGET_PATH ?= './data/silver'##@ [ingest] Opcional: Caminho de destino dos dados processados, por padrão './data/silver'.
INGEST_YEAR_MONTH ?= ##@ [ingest] Opcional: Partição YYYYMM. Se não fornecida, usa a ultima partição.
INGEST_USE_FAKE_DATA ?= ##@ [ingest] Opcional: Cria dados sinteticos. Se não fornecida, usa dados reais.
ingest: ## Faz a ingestão dos dados de uma determianda partição (mês)
	PYTHONPATH=src $(PYTHON) src/cli/ingest.py \
		--SOURCE_PATH $(SOURCE_PATH) \
		--TARGET_PATH $(INGEST_DATA_TARGET_PATH) \
		$(if $(INGEST_YEAR_MONTH),--YEAR_MONTH $(INGEST_YEAR_MONTH),) \
		$(if $(INGEST_USE_FAKE_DATA),--USE_FAKE_DATA $(INGEST_USE_FAKE_DATA),)