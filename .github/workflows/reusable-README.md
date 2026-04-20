# Reusable Workflows

Estes workflows são reutilizáveis para evitar duplicação de código nos GitHub Actions.
Devem estar no diretório raiz `.github/workflows/` (não em subpastas).

## reusable-setup-python.yml

Configura o ambiente Python completo:
- Checkout do código
- Setup do Python (versão configurável)
- Cache de dependências pip
- Instalação de dependências com extras configuráveis

**Inputs:**
- `python-version` (default: '3.13')
- `install-extras` (default: 'tests,dev')

**Outputs:**
- `python-version`

## reusable-lint-test.yml

Executa linting, formatação e testes completos:
- Checkout do código
- Setup do Python 3.13
- Cache de dependências
- Instalação de dependências [tests,dev]
- Lint com Ruff
- Format check com Black
- Type checking com Mypy
- Testes com cobertura mínima configurável
- Upload de coverage (opcional)

**Inputs:**
- `min-coverage` (default: '90')
- `upload-coverage` (default: true)

## reusable-create-pr.yml

Cria PRs automaticamente usando peter-evans/create-pull-request.

**Inputs:**
- `head-branch` (required)
- `base-branch` (required)
- `pr-title` (required)
- `pr-body` (required)

## Como usar

Nos workflows principais, chame com:

```yaml
jobs:
  my-job:
    uses: ./.github/workflows/reusable-setup-python.yml
    with:
      python-version: '3.13'
      install-extras: 'tests,dev'
```

## Benefícios

- DRY (Don't Repeat Yourself)
- Manutenção centralizada
- Consistência entre workflows
- Fácil de testar mudanças