from functools import lru_cache
from pathlib import Path
import secrets
import warnings

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "news2-hemodialysis-monitoring"
    database_url: str = Field(default="sqlite:///./news2_hemodialysis.db")
    auto_seed: bool = True
    static_dir: Path = Path(__file__).resolve().parent / "static"
    session_secret: str = Field(default="")
    session_cookie_name: str = "news2_session"
    session_max_age_seconds: int = 86400
    cookie_secure: bool = False
    allow_dev_role: bool = False
    default_admin_username: str = "admin"
    default_admin_password: str = "Admin@12345"
    force_admin_password_reset: bool = False

    def resolved_session_secret(self) -> str:
        if self.session_secret:
            return self.session_secret
        warnings.warn("NEWS2_SESSION_SECRET is not set; using an in-process development secret.", RuntimeWarning, stacklevel=2)
        return _DEV_SESSION_SECRET

    model_config = {
        "env_file": ".env",
        "env_prefix": "NEWS2_",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


_DEV_SESSION_SECRET = secrets.token_urlsafe(48)
