.PHONY: server server-debug


server: ## Inicia o servidor FastAPI via uvicorn
	PYTHONPATH=. $(PYTHON) -m src.app

server-debug: ## Inicia o servidor FastAPI via uvicorn em modo debug
	PYTHONPATH=. $(PYTHON) -m src.app --DEBUG=True