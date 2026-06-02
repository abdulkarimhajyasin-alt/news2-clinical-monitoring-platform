from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "news2-hemodialysis-monitoring"
    database_url: str = Field(default="sqlite:///./news2_hemodialysis.db")
    static_dir: Path = Path(__file__).resolve().parent / "static"

    model_config = {
        "env_file": ".env",
        "env_prefix": "NEWS2_",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
