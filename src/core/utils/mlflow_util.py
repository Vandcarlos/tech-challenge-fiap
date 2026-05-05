from functools import wraps

import mlflow


def mlflow_start_run(run_name: str | None = None, nested: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = run_name if run_name else func.__name__
            with mlflow.start_run(run_name=name, nested=nested):
                return func(*args, **kwargs)

        return wrapper

    return decorator
