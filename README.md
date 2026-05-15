# tech-challenge-fiap

Projeto de aula para o desafio FIAP Tech Challenge, com foco em:
- `pyproject.toml` como single source of truth
- setup de ambiente Python via `.venv`
- testes com cobertura mínima
- linting e formatação
- GitHub Actions para CI/CD

## Machine Learning Canvas: Previsão de Churn

| Campo | Descrição |
|-------|-----------|
| Value Proposition | Reduzir a perda de receita (Revenue Leakage) identificando clientes propensos a cancelar antes que o façam. |
| Stakeholders | Time de Retenção (Marketing), Gerência Financeira, Engenharia de Dados. |
| Métricas de Negócio | Redução da Taxa de Churn (%) e ROI das ações de retenção. |
| Data Sources | Histórico de chamadas, tipo de contrato, tempo de casa, métodos de pagamento e demografia. |
| SLOs (Técnico) | API com latência < 300ms; Disponibilidade 99%; Retreinamento mensal. |
| Baseline | Regressão Logística simples (Scikit-Learn) comparada à Rede Neural MLP.
## Estrutura do Projeto

- `src/` - código fonte do projeto
- `tests/` - testes com `pytest`
- `.github/workflows/` - GitHub Actions para PRs e deploys
- `Makefile` - comandos de setup, teste e ambiente
- `pyproject.toml` - dependências e configuração do projeto

## Requisitos

- Python 3.13+
- `make`
- `git`

A versão mínima suportada é definida em `.python-version`.

## Instalação

No root do projeto:

```bash
make setup-project
```

Isso cria `.venv` se necessário e instala as dependências principais.

Se quiser instalar tudo para desenvolvimento, incluindo testes e notebooks:

```bash
make setup-dev
```

Para instalar apenas dependências de testes:

```bash
make setup-tests
```

Para instalar apenas dependências de notebooks:

```bash
make setup-notebooks
```

## Ativar o ambiente

Após criar o venv, ative com:

```bash
source .venv/bin/activate
```

## Arquitetura do Sistema

O sistema de predição de churn utiliza uma arquitetura híbrida:

### Componentes Principais
- **Data Pipeline (Batch)**: Processamento de dados com PySpark e armazenamento em data lake (bronze/silver/gold)
- **Model Training**: Treinamento de modelo MLP com PyTorch, tracking via MLflow
- **Model Serving (Real-time)**: API FastAPI com inferência ONNX para predições em tempo real
- **Monitoramento**: Sistema de observabilidade com métricas, alertas e dashboards

### Tecnologias
- **Backend**: Python 3.12+, FastAPI, PySpark
- **ML**: PyTorch, ONNX Runtime, Scikit-learn
- **Dados**: Pandas, PySpark, Parquet
- **MLOps**: MLflow, Docker
- **DevOps**: GitHub Actions, Docker Compose

Para detalhes completos, consulte [docs/deploy_architecture.md](docs/deploy_architecture.md).

## Setup Completo do Projeto

### 1. Pré-requisitos
- Python 3.12+
- Docker e Docker Compose
- Git
- Make

### 2. Clonagem e Setup Inicial
```bash
git clone <repository-url>
cd tech-challenge-fiap
make setup-project
```

### 3. Setup de Serviços Externos
```bash
# Inicia MLflow e PostgreSQL
docker-compose -f devtools/docker-compose.yml up -d

# Verifica se os serviços estão rodando
docker-compose -f devtools/docker-compose.yml ps
```

### 4. Configuração de Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite as variáveis conforme necessário
# MLFLOW_HOST=http://localhost
# MLFLOW_PORT=5500
# MLFLOW_BACKEND_STORE_URI=postgresql+psycopg2://mlflow_user:mlflow_pass@postgres:5432/mlflow_db
# etc.
```

### 5. Acessos aos Serviços
- **MLflow UI**: http://localhost:5500
- **pgAdmin**: http://localhost:5050 (admin@admin.com / admin)
- **API da Aplicação**: http://localhost:8888

### 5. Setup de Desenvolvimento Completo
```bash
make setup-dev
```

## Execução do Sistema

### Pipeline de Dados (Batch)
```bash
# Ingestão de dados
python -m src.cli.ingest --SOURCE_PATH=./data/bronze --TARGET_PATH=./data/silver --YEAR_MONTH=202604

# Transformação para gold
python -m src.cli.ingest --SOURCE_PATH=./data/silver --TARGET_PATH=./data/gold --YEAR_MONTH=202604

# Treinamento do modelo
python -m src.cli.train --YEAR_MONTH=202604
```

### API de Predição (Real-time)
```bash
# Inicia o servidor
python src/app.py

# Ou com debug
python src/app.py --DEBUG=True
```

### Testes
```bash
# Todos os testes
make test

# Testes verbosos
make test-verbose

# Com cobertura específica
make test MIN_COVERAGE=85
```

### Notebooks
```bash
# Ative o ambiente e instale dependências
make setup-notebooks

# Execute Jupyter
jupyter lab notebooks/
```

## Endpoints da API

### Health Check
```bash
curl http://localhost:8888/health
```

### Predição de Churn
```bash
curl -X POST http://localhost:8888/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "gender": "Male",
      "senior_citizen": "No",
      "partner": "Yes",
      "dependents": "No",
      "tenure_months": 12,
      "phone_service": "Yes",
      "multiple_lines": "No",
      "internet_service": "Fiber optic",
      "online_security": "Yes",
      "online_backup": "No",
      "device_protection": "Yes",
      "tech_support": "No",
      "streaming_tv": "Yes",
      "streaming_movies": "Yes",
      "contract": "Month-to-month",
      "paperless_billing": "Yes",
      "payment_method": "Electronic check",
      "monthly_charges": 79.85,
      "total_charges": 1024.10
    }]
  }'
```

### Testes com Insomnia

Para facilitar os testes da API, importe o arquivo `devtools/Insomnia.yaml` no Insomnia:

1. Abra o Insomnia
2. File → Import Data → From File
3. Selecione `devtools/Insomnia.yaml`
4. Configure a variável `base_url` para `http://localhost:8888`

As requisições de exemplo estarão disponíveis na collection "FIAP_Tech_Challenge-Churn_Prediction".

## Model Card

Para informações completas sobre o modelo (performance, limitações, vieses), consulte [docs/model_card.md](docs/model_card.md).

## Monitoramento

O sistema inclui monitoramento abrangente. Para detalhes sobre métricas, alertas e playbook de resposta, consulte [docs/monitoring_plan.md](docs/monitoring_plan.md).

## Desenvolvimento

Esse projeto usa extras no `pyproject.toml`:

- `.[tests]` - dependências de teste
- `.[notebooks]` - dependências de notebooks
- `.[dev]` - linting e checagens estáticas

O `Makefile` instala `.[dev,tests,notebooks]` em `make setup-dev`.

### Qualidade de Código

- **Lint rápido**: `make lint` - executa ruff (lint + format check) em ~0.1s
- **Type check**: `make type-check` - executa mypy para verificação de tipos (mais lento)
- **Testes**: `make test` - executa pytest com cobertura

## Documentação

- **[Model Card](docs/model_card.md)**: Performance, limitações e vieses do modelo
- **[Arquitetura de Deploy](docs/deploy_architecture.md)**: Arquitetura híbrida batch/real-time
- **[Plano de Monitoramento](docs/monitoring_plan.md)**: Métricas, alertas e resposta a incidentes

## GitHub Actions

A pipeline configurada contém:

- criação automática de PR para `dev` a partir de branches `feature/*`, `chore/*` e `bugfix/*`
- criação automática de PR para `main` a partir de `dev`
- execução de build, lint e testes em PRs para `dev` e `main`
- execução completa em merge para `dev` e `main`
- placeholders de deploy com `echo deploy` para futuros ambientes

### Reusable Workflows

Para evitar duplicação, a pipeline usa reusable workflows no diretório `.github/workflows/`:

- `reusable-setup-python.yml` - setup completo do ambiente Python
- `reusable-lint-test.yml` - linting, formatação e testes com cobertura
- `reusable-create-pr.yml` - criação automática de PRs

## Observações

- Não use `requirements.txt`; a fonte única é `pyproject.toml`.
- Configurações de lint e teste estão centralizadas no `pyproject.toml`.
- Dados são armazenados em `data/` seguindo a estrutura de data lake
- Modelos treinados ficam em `models/train/` e modelos de produção em `models/predict/`
- Use Docker Compose para serviços auxiliares (MLflow, PostgreSQL)
- A arquitetura híbrida permite processamento batch eficiente e inferência real-time
- Configure as variáveis de ambiente do PostgreSQL para persistência do MLflow
