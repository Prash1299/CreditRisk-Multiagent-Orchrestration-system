from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    database_url: str = f"sqlite:///{(ROOT / 'data' / 'credit_risk.db').as_posix()}"
    redis_url: str = "redis://127.0.0.1:6379/0"
    chroma_path: str = str(ROOT / "data" / "chroma")
    credit_api_url: str = "http://127.0.0.1:8000"
    tavily_api_key: str = ""
    use_mcp: bool = False
    mcp_research_url: str = "http://127.0.0.1:8101/mcp"
    mcp_analyst_url: str = "http://127.0.0.1:8102/mcp"
    mcp_memory_url: str = "http://127.0.0.1:8103/mcp"
    celery_broker_url: str = ""
    celery_result_backend: str = ""

    @property
    def broker(self) -> str:
        return self.celery_broker_url or self.redis_url

    @property
    def result_backend(self) -> str:
        return self.celery_result_backend or self.redis_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
