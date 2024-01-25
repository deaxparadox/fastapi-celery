# Flower Dashboard

`Flower` is a lightweight, real-time, web-based monitoring tool for Celery. You can monitor currently running tasks, increase or decrease the worker pool, view graphs and a number of statistics, to name a few:

Add it to the requirements.txt

```
aiofiles==23.1.0
celery==5.2.7
fastapi==0.95.0
flower==1.2.0
Jinja2==3.1.2
pytest==7.2.2
redis==4.5.4
requests==2.28.2
uvicorn==0.21.1
httpx==0.23.3
```

Then, add a new service to `docker-compose.yml`:

```
dashboard:
  build: ./project
  command: celery --broker=redis://redis:6379/0 flower --port=5555
  ports:
    - 5556:5555
  environment:
    - CELERY_BROKER_URL=redis://redis:6379/0
    - CELERY_RESULT_BACKEND=redis://redis:6379/0
  depends_on:
    - web
    - redis
    - worker
```

Test it out:

```bash
$ docker compose up -d --build
```

Navigate to [http://localhost:5556](http://localhost:5556) to view the dashboard. You should see one worker ready to go:

