import pytest

from contextlib import contextmanager
from celery.result import EagerResult, AsyncResult

from celery_strategy.strategy import StrategyWrapper


@pytest.fixture(scope="session")
def celery_config(redis_url):
    return {
        "broker_url": redis_url,
        "result_backend": redis_url,
        "singleton_key_prefix": "lock_prefix:",
    }


@pytest.fixture(scope="session")
def celery_enable_logging():
    return True


@pytest.fixture
@contextmanager
def scoped_app(celery_app):
    yield celery_app


class TestSimpleTask:
    def test__handle_sync(self, scoped_app):
        with scoped_app as app:
            @app.task()
            def simple_task(*args):
                return args

            task = StrategyWrapper(simple_task).handle_sync()
            assert isinstance(task, EagerResult)

    def test__handle_async(self, scoped_app):
        with scoped_app as app:
            @app.task()
            def simple_task(*args):
                return args

            task = StrategyWrapper(simple_task).handle_async()
            assert isinstance(task, AsyncResult)

    @pytest.mark.celery(broker_url="redis://localhost")
    def test__handle__async(self, scoped_app, celery_worker):
        with scoped_app as app:
            @app.task()
            def simple_task(*args):
                return args

            task = StrategyWrapper(simple_task).handle()
            assert isinstance(task, AsyncResult)

    @pytest.mark.celery(broker_url="redis://localhost")
    def test__handle__sync(self, scoped_app, celery_worker):
        celery_worker.stop()

        with scoped_app as app:
            @app.task()
            def simple_task(*args):
                return args

            task = StrategyWrapper(simple_task).handle()
            assert isinstance(task, AsyncResult)


class TestTasksAttrs:
    def test__task__getattr(self, scoped_app):
        with scoped_app as app:
            name = 'simple_task'

            @app.task(name=name)
            def simple_task(*args):
                return args

            task_name = StrategyWrapper(simple_task).name
            assert task_name == name
