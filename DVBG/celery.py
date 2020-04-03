from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DVBG.settings')

app = Celery('worker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_default_queue = 'worker_queue'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
