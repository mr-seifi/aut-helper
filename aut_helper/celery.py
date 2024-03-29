import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aut_helper.settings')

app = Celery('aut_helper')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'update-food-prices': {
        'task': 'easy_food.tasks.update_foods_price',
        'schedule': crontab(minute='*/2'),
    },
    'update-books': {
        'task': 'easy_book.tasks.update_books',
        'schedule': crontab(minute='*/2'),
    }
}
