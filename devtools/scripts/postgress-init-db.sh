#!/bin/bash
set -e

echo "[INIT-DB] Iniciando varredura de variáveis de ambiente..."

# 1. Busca todas as variáveis que terminam com _POSTGRES_DB
# O sed remove o sufixo para pegar apenas o prefixo (ex: MLFLOW)
PREFIXES=$(env | grep '_POSTGRES_DB=' | sed 's/_POSTGRES_DB=.*//')

for PREFIX in $PREFIXES; do
    # 2. Tenta recuperar as 3 variáveis usando o prefixo encontrado
    DB_NAME=$(eval echo \$${PREFIX}_POSTGRES_DB)
    DB_USER=$(eval echo \$${PREFIX}_POSTGRES_USER)
    DB_PASS=$(eval echo \$${PREFIX}_POSTGRES_PASSWORD)

    # 3. Validação: Só cria se os 3 parâmetros existirem
    if [ -n "$DB_NAME" ] && [ -n "$DB_USER" ] && [ -n "$DB_PASS" ]; then
        echo "[INIT-DB] Criando stack para prefixo: $PREFIX"
        echo "          -> Database: $DB_NAME"
        echo "          -> User: $DB_USER"

        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
            CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
            CREATE DATABASE $DB_NAME;
            GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
            \c $DB_NAME
            GRANT ALL ON SCHEMA public TO $DB_USER;
EOSQL
    else
        echo "[INIT-DB] Ignorando prefixo $PREFIX: parâmetros incompletos."
    fi
done

echo "[INIT-DB] Processamento concluído."