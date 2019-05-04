from celery.task.control import inspect


def get_celery_worker_status():
    info = inspect()
    d = info.stats()  # type: dict
    if not d:
        d = {
            'message': 'No running Celery workers were found.',
            'status': False
        }
    else:
        d['status'] = True

    return d
