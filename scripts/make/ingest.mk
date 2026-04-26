.PHONY: ingest ingest-extract ingest-fake


YEAR_MONTH ?= ##@ [ingest] Opcional: Partição YYYY-MM. Se não fornecida, usa a ultima partição.
SOURCE_PATH ?= './data/bronze'##@ [ingest] Opcional: Caminho de origem dos dados, por padrão './data/bronze'.
DESTINATION_PATH ?= './data/silver'##@ [ingest] Opcional: Caminho de destino dos dados processados, por padrão './data/silver'.
ingest: ## Faz a ingestão dos dados de uma determianda partição (mês)
	PYTHONPATH=src $(PYTHON) src/data_ingest/local_job.py \
		$(if $(YEAR_MONTH),--YEAR_MONTH $(YEAR_MONTH),) \
		--SOURCE_PATH $(SOURCE_PATH) \
		--DESTINATION_PATH $(DESTINATION_PATH)

EXTRACT_YEAR_MONTH ?= ##@ [extract] Obrigatorio: Partição YYYY-MM para destino da extração.
EXTRACT_DESTINATION_PATH ?= './data/bronze'##@ [extract] Opcional: Caminho de destino dos dados extraídos, por padrão './data/bronze'.
ingest-extract: guard-EXTRACT_YEAR_MONTH ## Faz a extração da Kaggle e salva os dados extraídos no destino especificado
	PYTHONPATH=src $(PYTHON) src/data_ingest/extract.py \
		--YEAR_MONTH $(EXTRACT_YEAR_MONTH) \
		--DESTINATION_PATH $(EXTRACT_DESTINATION_PATH)


FAKE_YEAR_MONTH ?= ##@ [fake] Obrigatorio: Partição YYYY-MM para destino da extração.
FAKE_DESTINATION_PATH ?= './data/bronze'##@ [fake] Opcional: Caminho de destino dos dados fake, por padrão './data/bronze'.
ingest-fake: guard-FAKE_YEAR_MONTH ## Gera dados fake para a partição especificada
	PYTHONPATH=src $(PYTHON) src/data_ingest/fake_generator.py \
		--YEAR_MONTH $(FAKE_YEAR_MONTH) \
		--DESTINATION_PATH $(FAKE_DESTINATION_PATH)
