import time

from celery import shared_task


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    print('celery sleeping, ', task_type)
    return True