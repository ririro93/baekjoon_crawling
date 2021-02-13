import time

from celery import shared_task


@shared_task
def sample_task():
    return ('the sample task just ran')