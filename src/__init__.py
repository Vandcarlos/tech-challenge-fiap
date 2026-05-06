from .configs import configure_app

# A configuração do MLflow deve ser realizada explicitamente nos pontos de entrada
# da aplicação, evitando side-effects no momento de importação do pacote.
__all__ = ["configure_app"]
