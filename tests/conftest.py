import pytest
import os


@pytest.fixture(scope="session")
def redis_url():
    return os.environ.get(
        "CELERY_STRATEGY_TEST_REDIS_URL", "redis://localhost:63790"
    )
