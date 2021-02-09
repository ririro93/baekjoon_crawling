import celery
import os

app = celery.Celery('example')

@app.tast
def add(x, y):
    return x + y

app.conf.upate(BROKER_URL=os.environ['REDIS_URL'],
               CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])