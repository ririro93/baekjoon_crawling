import time

from celery import shared_task

from .views import *


# run this task every 2 minutes in the background
@shared_task
def background_crawling():
    return 'automatic background crawling finished'