from datetime import datetime
from logging import NOTSET, Logger, getLevelNamesMapping
from traceback import format_exception
from uuid import UUID

import structlog
from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from structlog.typing import FilteringBoundLogger
from uuid import uuid4
from opentelemetry.trace import (
    INVALID_SPAN,
    INVALID_SPAN_CONTEXT,
    get_current_span,
    get_tracer_provider,
)
from src.config import SERVICE_NAME


def get_request_id(request: Request) -> str:
    request_id = request.headers.get("X-Request-Id", "")
    if not request_id:
        request_id = str(uuid4())
    return request_id


def type_cast_to_str(logger: Logger, method_name: str, event_dict: dict) -> dict:
    provider = get_tracer_provider()
    service_name = None
    if service_name is None:
        resource = getattr(provider, "resource", None)
        if resource:
            service_name = (
                resource.attributes.get("service.name") or SERVICE_NAME
            )
        else:
            service_name = SERVICE_NAME

    if "event" in event_dict:
        event_dict["message"] = event_dict.pop("event")

    _event_dict = {}
    for k, v in event_dict.items():
        if isinstance(v, Exception) or issubclass(type(v), Exception):
            _event_dict[k] = str(v)
            _event_dict[f"{k}_traceback_dump"] = format_exception(
                type(v), v, v.__traceback__)
        else:
            _event_dict[k] = v

    span = get_current_span()
    if span != INVALID_SPAN:
        ctx = span.get_span_context()
        if ctx != INVALID_SPAN_CONTEXT:
            _event_dict["otelSpanID"] = ctx.span_id
            _event_dict["otelTraceID"] = ctx.trace_id
            _event_dict["otelServiceName"] = service_name
            _event_dict["otelTraceSampled"] = ctx.trace_flags.sampled

    return jsonable_encoder(_event_dict)


def add_time(logger: Logger, method_name: str, event_dict: dict):
    # * add time to log
    now = datetime.now()
    event_dict["time"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return type_cast_to_str(logger, method_name, event_dict)


LOG_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.TimeStamper(),
    structlog.processors.dict_tracebacks,
    # Add callsite parameters.
    structlog.processors.CallsiteParameterAdder(
        {
            structlog.processors.CallsiteParameter.PATHNAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        }
    ),
    add_time,
    structlog.processors.JSONRenderer(),
]


def get_logger() -> FilteringBoundLogger:
    structlog.configure(
        processors=LOG_PROCESSORS,
        wrapper_class=structlog.make_filtering_bound_logger(
            getLevelNamesMapping().get("INFO")
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    return structlog.get_logger()


def get_request_logger(
    request_id: UUID = Depends(get_request_id),
) -> FilteringBoundLogger:
    def log_processor(logger: Logger, log_method: str, event_dict: dict):
        event_dict["request_id"] = str(request_id)

        return type_cast_to_str(logger, log_method, event_dict)

    _log_processors = [*LOG_PROCESSORS]
    _log_processors.insert(-2, log_processor)

    structlog.configure(
        processors=_log_processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getLevelNamesMapping().get("INFO")
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    return structlog.get_logger()
