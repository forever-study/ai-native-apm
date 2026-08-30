from pydantic_settings import BaseSettings


class OtelSettings(BaseSettings):
    otel_enabled: bool = False
    otel_service_name: str = "ai_native_apm"
    otel_console_exporter_enabled: bool = False
