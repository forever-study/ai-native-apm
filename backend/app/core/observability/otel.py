import logging

from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogRecordExporter,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.semconv.attributes import service_attributes

from app.config import settings

logger = logging.getLogger(__name__)


class OTelInitializer:
    """编排 OTel SDK 的初始化：Resource / Tracer / Meter / Logger + 自动埋点。"""

    def __init__(self) -> None:
        self.tracer_provider: TracerProvider | None = None
        self.meter_provider: MeterProvider | None = None
        self.logger_provider: LoggerProvider | None = None

    def _create_resource(self) -> Resource:
        return Resource.create(
            {service_attributes.SERVICE_NAME: settings.otel.otel_service_name}
        )

    def _setup_tracer(self, resource: Resource) -> None:
        self.tracer_provider = TracerProvider(resource=resource)
        if settings.otel.otel_console_exporter_enabled:
            self.tracer_provider.add_span_processor(
                SimpleSpanProcessor(ConsoleSpanExporter())
            )
        else:
            self.tracer_provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter())
            )
        trace.set_tracer_provider(self.tracer_provider)

    def _setup_meter(self, resource: Resource) -> None:
        if settings.otel.otel_console_exporter_enabled:
            metric_readers = [PeriodicExportingMetricReader(ConsoleMetricExporter())]
        else:
            metric_readers = [PeriodicExportingMetricReader(OTLPMetricExporter())]
        self.meter_provider = MeterProvider(
            metric_readers=metric_readers, resource=resource
        )
        metrics.set_meter_provider(self.meter_provider)

    def _setup_logger(self, resource: Resource) -> None:
        self.logger_provider = LoggerProvider(resource=resource)

        if settings.otel.otel_console_exporter_enabled:
            self.logger_provider.add_log_record_processor(
                SimpleLogRecordProcessor(ConsoleLogRecordExporter())
            )
        else:
            self.logger_provider.add_log_record_processor(
                BatchLogRecordProcessor(OTLPLogExporter())
            )

        handler = LoggingHandler(
            level=logging.NOTSET, logger_provider=self.logger_provider
        )
        logging.getLogger("root").addHandler(handler)

    def _setup_instrumentors(self, app: FastAPI) -> None:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor.instrument_app(app, excluded_urls="/v1/traces$")

    def setup(self, app: FastAPI) -> None:
        if not settings.otel.otel_enabled:
            return
        resource = self._create_resource()
        self._setup_tracer(resource)
        self._setup_meter(resource)
        self._setup_logger(resource)
        self._setup_instrumentors(app)
        logger.info("Setting up OpenTelemetry Success")

    def stop(self) -> None:
        if self.tracer_provider is not None:
            self.tracer_provider.shutdown()
            self.tracer_provider = None
        if self.meter_provider is not None:
            self.meter_provider.shutdown()
            self.meter_provider = None
        if self.logger_provider is not None:
            self.logger_provider.shutdown()
            self.logger_provider = None


otel_initializer = OTelInitializer()
