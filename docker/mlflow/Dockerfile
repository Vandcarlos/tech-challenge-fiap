# Dockerfile for MLflow server on AWS ECS
FROM ghcr.io/mlflow/mlflow:v3.1.1

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# DB driver + S3 client
RUN pip install --no-cache-dir \
    psycopg2==2.9.9 \
    boto3==1.35.0

# Expose MLflow UI port
EXPOSE 5000

# Use bash so we can expand env vars
SHELL ["/bin/bash", "-lc"]

# Copy custom entrypoint
COPY docker/mlflow/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
