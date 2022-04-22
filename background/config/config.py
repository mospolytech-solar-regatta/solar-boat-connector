import os

enable_utc = True
timezone = 'Europe/Moscow'
broker_url = os.environ.get('REDIS_DSN')
include = ['background.tasks']
task_cls = 'background.tasks:SerialTask'
worker_concurrency = 1

beat_schedule = {
    'read-serial': {
        'task': 'background.tasks.read_data',
        'schedule': 0.5,
    },
}