# Trigger a Task

Update the route handler in *main.py* to kickoff the task and respond with the task ID:


```py
@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})
```

Don't forget to import the task:

```py
from worker import create_task
```

Build the image immages and spin up the new containers:

```bash
$ docker compose up -d --build
```

To trigger a new task,run:

```bash
$ curl http://localhost:8004/tasks -H "Content-Type: application/json" -d '{"type": 0}'
```

Output:

```bash
{"task_id":"24db9f54-6cac-4b6f-bf26-eff45ae966fd"}
```
