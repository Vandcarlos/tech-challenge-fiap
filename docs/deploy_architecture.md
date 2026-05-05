# Arquitetura de Deploy: Churn Prediction System

## Visão Geral

O sistema de predição de churn adota uma arquitetura híbrida combinando processamento batch para ingestão e treinamento de dados com inferência em tempo real para predições on-demand. Esta abordagem permite balancear eficiência de processamento em larga escala com baixa latência para casos de uso interativos.

## Componentes da Arquitetura

### 1. Camada de Dados (Data Lake)
- **Bronze Layer**: Dados brutos ingeridos via Spark
- **Silver Layer**: Dados limpos e transformados
- **Gold Layer**: Dados agregados e prontos para modelagem

### 2. Pipeline de Batch (ETL/Training)
- **Tecnologias**: PySpark, Pandas, MLflow
- **Execução**: Jobs locais ou em containers Docker
- **Armazenamento**: Parquet files no data lake
- **Orquestração**: Scripts CLI para execução manual/automatizada

### 3. Serviço de Inferência (Real-time)
- **API**: FastAPI com endpoints REST
- **Modelo**: ONNX Runtime para inferência otimizada
- **Cache**: Modelos carregados em memória
- **Monitoramento**: Health checks e métricas de performance

### 4. Monitoramento e Observabilidade
- **Logs**: Structured logging com Python logging
- **Métricas**: Latência, throughput, error rates
- **Alertas**: Thresholds configuráveis para degradação

## Justificativa da Arquitetura Escolhida

### Por que Híbrida (Batch + Real-time)?

1. **Eficiência de Processamento**:
   - Batch processing permite lidar com grandes volumes de dados históricos
   - Otimizado para transformações complexas e treinamento de modelos

2. **Baixa Latência para Inferência**:
   - Real-time serving garante respostas rápidas (< 300ms SLO)
   - Essencial para integração com sistemas de CRM/marketing

3. **Custos Operacionais**:
   - Batch jobs podem ser executados em horários off-peak
   - Real-time services mantêm recursos alocados para disponibilidade

4. **Manutenibilidade**:
   - Separação clara entre pipelines de dados e serving
   - Facilita updates independentes de componentes

### Comparação com Alternativas

#### Batch-only
- **Prós**: Simples, custo-efetivo para predições periódicas
- **Contras**: Alta latência, não adequado para casos de uso interativos

#### Real-time-only
- **Prós**: Baixa latência, integração fácil com aplicações
- **Contras**: Complexidade de processamento de grandes volumes, custos elevados

#### Lambda Architecture
- **Prós**: Combina velocidade e throughput
- **Contras**: Complexidade de manutenção de dois pipelines paralelos

## Infraestrutura de Deploy

### Ambiente de Desenvolvimento
- **Local**: Python venv, Docker Compose para serviços auxiliares
- **CI/CD**: GitHub Actions para testes e linting

### Ambiente de Produção
- **Containerização**: Docker para isolamento e portabilidade
- **Orquestração**: Docker Compose para serviços locais
- **Cloud-ready**: Configurado para deploy em plataformas cloud

### Dependências Externas
- **MLflow**: Tracking de experimentos e modelos
- **PostgreSQL**: Metadata store (via Docker Compose)
- **MinIO**: Artifact store (opcional)

## Estratégia de Deploy

### Blue-Green Deployment
- Zero-downtime updates através de versionamento de modelos
- Rollback automático em caso de falhas

### Canary Releases
- Deploy gradual para subset de tráfego
- Monitoramento de métricas para validação

### Rollback Strategy
- Versionamento de modelos permite rollback instantâneo
- Cache de modelos anteriores mantido por período de graça

## Segurança

### Autenticação e Autorização
- API keys para acesso aos endpoints
- Rate limiting para proteção contra abuso

### Dados Sensíveis
- Dados de clientes tratados conforme LGPD
- Encriptação em trânsito e repouso

### Auditoria
- Logs de acesso e predições para compliance
- Rastreabilidade de mudanças em modelos

## Escalabilidade

### Horizontal Scaling
- API stateless permite múltiplas instâncias
- Load balancer para distribuição de carga

### Vertical Scaling
- Otimização de modelo ONNX para eficiência
- Cache inteligente de modelos

### Auto-scaling
- Baseado em métricas de CPU/memória
- Thresholds configuráveis por ambiente