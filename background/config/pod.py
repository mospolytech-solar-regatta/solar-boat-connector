import os

enable_utc = True
timezone = 'Europe/Moscow'
broker_url = os.environ.get('REDIS_DSN')
include = ['background.tasks']
task_cls = 'background.tasks:SerialTask'
worker_concurrency = 1
result_backend = 'rpc://'
result_persistent = False

beat_schedule = {
    'read-serial': {
        'task': 'background.tasks.read_data',
        'schedule': 1,
    },
}
