from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cwwed.settings')

REDIS_URL = 'redis://{}'.format(os.environ.get('CELERY_BROKER', ''))

app = Celery(
    'cwwed',
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# scheduled jobs
app.conf.beat_schedule = {
    'DEM updater': {
        'task': 'dems.tasks.update_dems_task',
        'schedule': 60 * 60 * 24,
    },
}
