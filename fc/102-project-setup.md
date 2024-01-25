# Project Setup

```bash
$ git clone https://github.com/deaxparadox/fastapi-celery --branch v1 --single-branch
$ cd fastapi-celery
$ git checkout v1 -b master
```

Since we'll need to manage three processes in total (FastAPI, Redis, Celery worker), we'll use Docker to simplify our workflow by wiring them up so that they can all be run from one terminal window with a single command.

From the project root, create the images and spin up the Docker containers:

```bash
$ docker compose up --build
```

for detach mode:

```bash
$ docker compose up -d --build
```

Once the build is complete, navigate to [http://localhost:8004](http://localhost:8004):


Make sure the tests pass as well:

```bash
$ docker compose exec web python -m pytest
=============================== test session starts ================================
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.4.0
rootdir: /usr/src/app
plugins: anyio-4.2.0
collected 1 item                                                                   

tests/test_tasks.py .                                                        [100%]

================================ 1 passed in 0.08s =================================
```
----------


