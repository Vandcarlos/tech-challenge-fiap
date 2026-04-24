#!/bin/sh

# O arquivo .pgpass deve ter o formato: hostname:port:database:username:password
# Usamos as variáveis que já estão no seu .env e mapeadas no compose
echo "postgres:5432:*:${POSTGRES_USER}:${POSTGRES_PASSWORD}" > /tmp/pgpassfile

# O pgAdmin exige que o arquivo de senha tenha permissões restritas (0600)
chmod 600 /tmp/pgpassfile
echo "[PGADMIN-SETUP] .pgpass gerado com sucesso."

# Executa o entrypoint original da imagem do pgAdmin
exec /entrypoint.sh