import logging
import time
from typing import Callable

from fastapi import FastAPI, Request

from src.domain import APIMetrics

logger = logging.getLogger(__name__)

# Cache em memória, localmente vou migrar para SQLite, na aws usaria o Redis
LATENCY_HISTORY: list[float] = []


def register_observability(app: FastAPI):
    @app.middleware("http")
    async def log_latency_middleware(request: Request, call_next: Callable):
        start_time = time.time()

        response = await call_next(request)

        if request.url.path != "/health":
            duration = time.time() - start_time
            LATENCY_HISTORY.append(duration)

            if len(LATENCY_HISTORY) > 50:
                LATENCY_HISTORY.pop(0)

            logger.info(
                f"Method: {request.method}\n"
                f"Path: {request.url.path}\n"
                f"Status: {response.status_code}\n"
                f"Duration: {duration:.4f}s"
            )

            response.headers["X-Response-Time"] = str(duration)

        return response


def get_metrics() -> APIMetrics:
    if not LATENCY_HISTORY:
        return APIMetrics()

    count = len(LATENCY_HISTORY)
    total_sum = sum(LATENCY_HISTORY)

    return APIMetrics(
        avg_latency=round(total_sum / count, 4),
        last_latency=round(LATENCY_HISTORY[-1], 4),
        total_requests=len(LATENCY_HISTORY),
    )
