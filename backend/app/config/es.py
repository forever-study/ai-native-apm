from pydantic_settings import BaseSettings


class EsSettings(BaseSettings):
    es_enabled: bool = True
    elasticsearch_url: str = "http://localhost:9200"
    elastic_api_key: str = ""
