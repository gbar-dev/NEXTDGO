from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')

redis_password = os.getenv("REDIS_PASSWORD", "")
app.conf.broker_url = f'redis://:{redis_password}@redis:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_scheduler = 'celery.beat.PersistentScheduler'

app.autodiscover_tasks()