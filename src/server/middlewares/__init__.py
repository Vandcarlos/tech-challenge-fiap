from fastapi import FastAPI

from .observability import register_observability


def register_middlewares(app: FastAPI):
    register_observability(app)


__all__ = ["register_middlewares"]
