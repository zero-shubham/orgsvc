from src.application import app
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from fastapi import Request


from src.config import OLTP_HTTP_TRACE_ENDPOINT, OLTP_HTTP_METER_ENDPOINT


resource = Resource.create({
    "service.name": "orgsvc"
})

trace_provider = TracerProvider(
    resource=resource,
)

meter_provider = MeterProvider(
    metric_readers=[PeriodicExportingMetricReader(
        exporter=OTLPMetricExporter(endpoint=OLTP_HTTP_METER_ENDPOINT),
        export_interval_millis=1000  # Export every 3 seconds
    )],
    resource=resource,
)
metrics.set_meter_provider(meter_provider=meter_provider)

processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=OLTP_HTTP_TRACE_ENDPOINT))
trace_provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(trace_provider)


meter = metrics.get_meter("orgsvc", meter_provider=meter_provider)

req_counter = meter.create_counter(
    "request_counter", unit="1", description="Counts the  total requests served"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    req_counter.add(1, {"request.url": request.url.path})
    return await call_next(request)


AsyncPGInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(
    app=app, tracer_provider=trace_provider, meter_provider=meter_provider)
LoggingInstrumentor().instrument()  # set OTEL_PYTHON_LOG_CORRELATION=true
