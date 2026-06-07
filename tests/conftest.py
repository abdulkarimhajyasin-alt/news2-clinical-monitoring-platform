import pytest

from app.config import get_settings


@pytest.fixture(autouse=True)
def enable_dev_role_for_legacy_tests(monkeypatch):
    monkeypatch.setenv("NEWS2_ALLOW_DEV_ROLE", "true")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
