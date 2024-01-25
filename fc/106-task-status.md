# Task Status

Turn back to the `handleClick` function on the client-side:

```javascript
function handleClick(type) {
  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ type: type }),
  })
  .then(response => response.json())
  .then(res => getStatus(res.data.task_id));
}
```

When the response comes back from the original AJAX request, we then continue to call `getStatus()` with the task ID every second:

```javascript
function getStatus(taskID) {
  fetch(`/tasks/${taskID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    const html = `
      <tr>
        <td>${taskID}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`;
    document.getElementById('tasks').prepend(html);
    const newRow = document.getElementById('table').insertRow();
    newRow.innerHTML = html;
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .catch(err => console.log(err));
}
```

If the response is successfull, a new row is added to the table on the DOM:

Update the `get_status` route handler to return the status:

```py
@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
```

import `AsyncResult`:

```py
from celery.result import AsyncResult
```

Update the containers:

```bash
$ docker compose up -d --build
```

Trigger a new task:

```bash
$ curl http://localhost:8004/tasks -H "Content-Type: application/json" --data '{"type": 1}'
```

Then, grab the `task_id` from the response and call the updated endpoint to view the status:

```bash
$ curl http://localhost:8004/tasks/f3ae36f1-58b8-4c2b-bf5b-739c80e9d7ff

{
  "task_id": "455234e0-f0ea-4a39-bbe9-e3947e248503",
  "task_result": true,
  "task_status": "SUCCESS"
}
```