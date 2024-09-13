import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tech.settings')

app = Celery('tech')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'every': { 
        'task': 'main.tasks.checkFinishDate',
        'schedule': crontab(),
    },

}