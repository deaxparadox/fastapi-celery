# Celery Logs

Update the `worker` service, in *docker-compose.yml*, so that Celery logs are dumped to a log file:

```
worker:
  build: ./project
  command: celery -A worker.celery worker --loglevel=info --logfile=logs/celery.log
  volumes:
    - ./project:/usr/src/app
  environment:
    - CELERY_BROKER_URL=redis://redis:6379/0
    - CELERY_RESULT_BACKEND=redis://redis:6379/0
  depends_on:
    - web
    - redis
```

Add a new directory to "project" called "logs". Then, add a new file called *celery.log* to that newly created directory.

Update:

```bash
$ docker compose up --build
```

You should see the log file fill up the locally since we set up a volumn:

```
[2023-04-05 16:10:33,257: INFO/MainProcess] Connected to redis://redis:6379/0
[2023-04-05 16:10:33,262: INFO/MainProcess] mingle: searching for neighbors
[2023-04-05 16:10:34,271: INFO/MainProcess] mingle: all alone
[2023-04-05 16:10:34,283: INFO/MainProcess] celery@6ea5007507db ready.
[2023-04-05 16:11:49,400: INFO/MainProcess]
  Task create_task[7f0022ec-bcc8-4eff-b825-bde60d15f824] received
[2023-04-05 16:11:59,418: INFO/ForkPoolWorker-7]
  Task create_task[7f0022ec-bcc8-4eff-b825-bde60d15f824]
  succeeded in 10.015363933052868s: True
```