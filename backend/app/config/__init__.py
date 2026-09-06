from .es import EsSettings
from .otel import OtelSettings


class Settings:
    def __init__(self) -> None:
        self.otel: OtelSettings = OtelSettings()
        self.es: EsSettings = EsSettings()


settings = Settings()
