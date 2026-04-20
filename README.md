# tech-challenge-fiap

Projeto de aula para o desafio FIAP Tech Challenge, com foco em:
- `pyproject.toml` como single source of truth
- setup de ambiente Python via `.venv`
- testes com cobertura mínima
- linting e formatação
- GitHub Actions para CI/CD

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

## Execução

Rode o projeto localmente com:

```bash
python src/helloworld.py
```

## Testes

Executar a suíte de testes e cobertura:

```bash
make test
```

O alvo `test` exige cobertura mínima de 90% por padrão.

Para rodar em modo verboso:

```bash
make test-verbose
```

Para alterar a cobertura mínima:

```bash
make test MIN_COVERAGE=85
```

## Desenvolvimento

Esse projeto usa extras no `pyproject.toml`:

- `.[tests]` - dependências de teste
- `.[notebooks]` - dependências de notebooks
- `.[dev]` - linting e checagens estáticas

O `Makefile` instala `.[dev,tests,notebooks]` em `make setup-dev`.

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
