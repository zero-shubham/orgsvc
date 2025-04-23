from contextlib import asynccontextmanager
from src.db import init_db, run_migrations, DATABASE_URL
from fastapi import FastAPI
from src.application import app
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


AsyncPGInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(app=app)
LoggingInstrumentor().instrument()  # set OTEL_PYTHON_LOG_CORRELATION=true

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await run_migrations("./migrations", DATABASE_URL)
    yield
