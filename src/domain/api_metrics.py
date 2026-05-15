from dataclasses import dataclass


@dataclass
class APIMetrics:
    avg_latency: float = 0
    last_latency: float = 0
    total_requests: int = 0
