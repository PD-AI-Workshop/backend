from fastapi import Request
from prometheus_client import CollectorRegistry, Counter, Gauge

custom_registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_class"],
    registry=custom_registry
)

ERROR_COUNT = Counter(
    "http_5xx_errors_total",
    "Total 5xx Server Errors",
    ["method", "endpoint"],
    registry=custom_registry
)

REQUEST_2XX_GAUGE = Gauge(
    "http_2xx_percentage",
    "Percentage of 2xx Successful Requests",
    registry=custom_registry
)

REQUEST_5XX_GAUGE = Gauge(
    "http_5xx_percentage",
    "Percentage of 5xx Server Errors",
    registry=custom_registry
)

async def metrics_middleware(request: Request, call_next):
    if request.url.path in ["/metrics", "/custom-metrics"]:
        return await call_next(request)
    
    response = await call_next(request)
    status_class = f"{response.status_code // 100}xx"
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status_class=status_class).inc()
    
    if status_class == "5xx":
        ERROR_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    
    return response