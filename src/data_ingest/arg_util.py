"""Utils para parsing de argumentos de linha de comando."""

import sys


def get_arg(name: str) -> str | None:
    """
    Busca um argumento no formato --NAME no sys.argv.
    Se não encontrar, retorna None.
    """
    prefix = f"--{name}"
    for i, arg in enumerate(sys.argv):
        if arg == prefix and i + 1 < len(sys.argv):
            return sys.argv[i + 1]

    return None
