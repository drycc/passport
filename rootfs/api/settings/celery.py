import os

from kombu import Exchange, Queue
from celery import Celery


class Config(object):
    # Celery Configuration Options
    enable_utc = True
    task_serializer = 'pickle'
    accept_content = frozenset([
        'application/data',
        'application/json',
        'application/text',
        'application/x-python-serialize',
    ])
    task_track_started = True
    task_time_limit = 5 * 60
    worker_max_tasks_per_child = 200
    worker_prefetch_multiplier = 1
    result_expires = 24 * 60 * 60
    cache_backend = 'django-cache'
    task_default_queue = 'passport.notifications'
    task_default_exchange = 'passport.priority'
    task_default_routing_key = 'passport.priority.notifications'
    broker_transport_options = {"queue_order_strategy": "sorted"}
    task_create_missing_queues = True
    task_inherit_parent_priority = True
    broker_connection_retry_on_startup = True
    worker_cancel_long_running_tasks_on_connection_loss = True


app = Celery('passport')
app.config_from_object(Config())
app.conf.update(
    timezone=os.environ.get('TZ', 'UTC'),
    task_routes={
        'api.tasks.send_notification': {
            'queue': 'passport.notifications',
            'exchange': 'passport.priority', 'routing_key': 'passport.priority.notifications',
        },
    },
    task_queues=(
        Queue(
            'passport.notifications', exchange=Exchange('passport.priority', type="direct"),
            routing_key='passport.priority.notifications',
        ),
    ),
)
DRYCC_VALKEY_URL = os.environ.get('DRYCC_VALKEY_URL', 'redis://:@127.0.0.1:6379')
app.conf.update(
    broker_url=DRYCC_VALKEY_URL,
    result_backend=DRYCC_VALKEY_URL,
    broker_transport_options={"queue_order_strategy": "sorted", "visibility_timeout": 43200},
)
app.autodiscover_tasks()
