# Celery Setup

Start by added both Celery and Redis to the *requirements.txt* file:

```
aiofiles==23.1.0
celery==5.2.7
fastapi==0.95.0
Jinja2==3.1.2
pytest==7.2.2
redis==4.5.4
requests==2.28.2
uvicorn==0.21.1
httpx==0.23.3
```

Celery uses a message broker -- `RabbitMQ`, `Redis`, or `AWS Simple Queue Service (SQS)` -- to facilitate communication between the Celery worker and the web application. Messages are added to the broker, which are then processed by the worker(s). Once done, the results are added to the backend.

`Redis` will be used as both the broker and backend. Add both Redis and a Celery worker to the *docker-compose.yml* file like so:

```
version: '3.8'

services:

  web:
    build: ./project
    ports:
      - 8004:8000
    command: uvicorn main:app --host 0.0.0.0 --reload
    volumes:
      - ./project:/usr/src/app
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis

  worker:
    build: ./project
    command: celery -A worker.celery worker --loglevel=info
    volumes:
      - ./project:/usr/src/app
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - web
      - redis

  redis:
    image: redis:7
```

Take note of `celery -A worker.celery worker --loglevel=info`:

1. `celery worker` is used to start a Celery `worker`
2. `-A worker.celery` runs the Celery Application (`which we'll define shortly`)
3. `--loglevel=info` sets the `logging level` to info


Next, create a new file called *worker.py* in "project":

```py
import os
import time

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
```

Here, we created a new Celery instance, and using the `task` decorator, we defined a new Celery task function called `create_task`.