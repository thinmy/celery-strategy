from .utils import get_celery_worker_status


class StrategyWrapper(object):
    """
    Wrapper for define strategy when calling a celery background task.

    Uses argument to define how to process a task from celery.
    Uses configuration from application to define strategy.
    """

    def __init__(self, task, *args, **kwargs):
        self._task = task
        self._strategy = kwargs.pop('strategy', None)

    def __getattr__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return getattr(self._task, item)

    def get_strategy(self, *args, **kwargs):
        """
        Process task based on celery inspection, check if has at least one
        running worker.

        :param args:
        :param kwargs:
        :return:
        """
        worker_status = get_celery_worker_status()
        if worker_status['status']:
            return getattr(self, 'handle_async')(*args, **kwargs)

        return getattr(self, 'handle_sync')(*args, **kwargs)

    def handle(self, *args, **kwargs):
        """
        Process task based on self definition.

        :param args:
        :param kwargs:
        :return:
        """
        return self.get_strategy(*args, **kwargs)

    def handle_sync(self, *args, **kwargs):
        """
        Process task synchronous.

        :param args:
        :param kwargs:
        :return:
        """
        return self._task.apply(*args, **kwargs)

    def handle_async(self, *args, **kwargs):
        """
        Process task asynchronous.

        :param args:
        :param kwargs:
        :return:
        """
        return self._task.apply_async(*args, **kwargs)
