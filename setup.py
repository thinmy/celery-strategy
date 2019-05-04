from setuptools import setup

setup(
    name='celery-strategy',
    version='0.0.1',
    description='Don`t lose any task when celery is offline or not responding.',
    author='Thinmy Patrick Alves',
    author_email='thinmy@gmail.com',
    url='https://github.com/thinmy/celery-strategy',
    license='MIT',
    install_requires=[
        'celery>=4.0.0',
        'redis>=2.10.5'
    ],
    packages=['celery_strategy']
)
