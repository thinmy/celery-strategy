import pytest

from contextlib import contextmanager

from celery_strategy.utils import get_celery_worker_status


@pytest.fixture(scope="session")
def celery_config(redis_url):
    return {
        "broker_url": redis_url,
        "result_backend": redis_url
    }


@pytest.fixture(scope="session")
def celery_enable_logging():
    return True


@pytest.fixture
@contextmanager
def scoped_app(celery_app):
    yield celery_app


class TestUtils:
    @pytest.mark.celery(broker_url="redis://localhost")
    def test__get_celery_worker_status(self, scoped_app, celery_worker):
        with scoped_app as app:
            info = get_celery_worker_status()
            assert info['status']

    @pytest.mark.celery(broker_url="redis://localhost")
    def test__get_celery_worker_status_false(self, scoped_app, celery_worker):
        celery_worker.stop()

        with scoped_app as app:
            info = get_celery_worker_status()
            assert not info['status']
