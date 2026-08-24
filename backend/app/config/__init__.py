from .otel import OtelSettings


class Settings:
    def __init__(self) -> None:
        self.otel = OtelSettings()


settings = Settings()
