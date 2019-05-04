import pytest
from contextlib import contextmanager
from celery.backends.redis import RedisBackend


def clear_locks(backend):
    backend.clear("CELERY_STRATEGY_TASK_PREFIX_")


@pytest.fixture
@contextmanager
def backend(redis_url):
    backend = RedisBackend(redis_url)
    try:
        yield backend
    finally:
        clear_locks(backend)


class FakeBackend:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


@pytest.fixture(scope="function")
def fake_config():
    class FakeConfig:
        backend_url = "redis://localhost"
        backend_kwargs = {}
        backend_class = FakeBackend

    return FakeConfig()
