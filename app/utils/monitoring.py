"""
Prometheus monitoring setup for Arithmos Service.
Starts an HTTP server to expose metrics and provides common metrics collectors.
"""
import os
from prometheus_client import start_http_server, Counter, Summary, Gauge

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'arithmos_requests_total',
    'Total number of requests received',
    ['endpoint']
)

REQUEST_LATENCY = Summary(
    'arithmos_request_latency_seconds',
    'Latency of requests in seconds',
    ['endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'arithmos_active_requests',
    'Number of active (in-flight) requests'
)


def start_metrics_server():
    """
    Start Prometheus metrics HTTP server on given port (default from METRICS_PORT env or 8001).
    """
    port = int(os.getenv('METRICS_PORT', 8001))
    start_http_server(port)