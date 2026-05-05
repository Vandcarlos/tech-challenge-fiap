# Model Card: Churn Prediction MLP

## Visão Geral do Modelo

Este modelo é uma rede neural MLP (Multi-Layer Perceptron) treinada para prever a probabilidade de churn de clientes de telecomunicações. O modelo foi desenvolvido como parte do Tech Challenge FIAP, utilizando dados históricos de clientes incluindo informações demográficas, serviços contratados e histórico de pagamentos.

### Tipo de Modelo
- **Arquitetura**: Rede Neural MLP com camadas densas
- **Framework**: PyTorch, convertido para ONNX para inferência
- **Tarefa**: Classificação binária (churn: sim/não)
- **Formato de Entrada**: Dados tabulares preprocessados (features numéricas e categóricas codificadas)

## Performance

### Métricas Principais (Conjunto de Teste)

| Métrica | Valor |
|---------|-------|
| Accuracy | 0.798 |
| Precision (Weighted) | 0.797 |
| Recall (Weighted) | 0.798 |
| F1-Score (Weighted) | 0.797 |
| AUC-ROC | 0.846 |
| PR-AUC | 0.652 |

### Métricas por Classe

#### Classe 0 (Não-Churn)
- Precision: 0.83
- Recall: 0.88
- F1-Score: 0.85

#### Classe 1 (Churn)
- Precision: 0.66
- Recall: 0.61
- F1-Score: 0.63

## Limitações

### Limitações Técnicas
- **Dados de Treinamento**: Modelo treinado com dados históricos até 2024, pode não generalizar bem para mudanças futuras no comportamento dos clientes
- **Features Disponíveis**: Limitado às features presentes no dataset fornecido, não inclui dados comportamentais em tempo real
- **Latência**: Modelo ONNX otimizado para inferência rápida, mas pode ter limitações em ambientes com recursos limitados

### Cenários de Falha
- **Dados Faltantes**: Modelo pode falhar se features obrigatórias estiverem ausentes
- **Outliers**: Valores extremos em features numéricas podem degradar performance
- **Distribuição de Dados**: Mudanças significativas na distribuição dos dados podem reduzir accuracy
- **Viés Temporal**: Modelo pode perder performance ao longo do tempo devido a mudanças no mercado

## Viéses

### Viéses Potenciais
- **Demográfico**: Dataset pode ter viéses relacionados a gênero, idade ou localização geográfica
- **Socioeconômico**: Features como tipo de contrato e método de pagamento podem refletir viéses socioeconômicos
- **Seleção**: Dados históricos podem não representar adequadamente novos segmentos de clientes

### Mitigações Implementadas
- **Preprocessamento**: Uso de técnicas de encoding apropriadas para variáveis categóricas
- **Validação Cruzada**: Avaliação em conjunto de teste separado para evitar overfitting
- **Monitoramento**: Implementação de monitoramento contínuo para detectar drift de dados

## Uso Recomendado

### Casos de Uso Adequados
- **Pontuação de Risco**: Avaliação probabilística de churn para campanhas de retenção
- **Segmentação**: Identificação de grupos de alto risco para ações preventivas
- **Análise de Cenários**: Simulação de impacto de mudanças em serviços

### Casos de Uso Não Recomendados
- **Decisões Automáticas Críticas**: Não deve ser usado como única fonte para decisões de cancelamento de serviços
- **Aplicações em Tempo Real Críticas**: Latência pode não atender requisitos de sistemas críticos
- **Dados Fora do Domínio**: Não aplicar a dados muito diferentes do conjunto de treinamento

## Manutenção

### Retraining
- **Frequência**: Mensal, baseado em novos dados disponíveis
- **Triggers**: Degradação de performance > 5% ou drift de dados detectado
- **Pipeline**: Automatizado via GitHub Actions e MLflow

### Versionamento
- **MLflow**: Controle de versão de modelos e experimentos
- **Git**: Versionamento de código e configurações
- **Docker**: Versionamento de ambientes de produção

## Contato

Para questões sobre o modelo, entre em contato com a equipe de MLOps da FIAP Tech Challenge.