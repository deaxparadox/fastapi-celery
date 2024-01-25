# Trigger a Task


An `onclick` event handler in *project/templates/home.html* is set up that listens for a button click:

```html
<div class="btn-group" role="group" aria-label="Basic example">
  <button type="button" class="btn btn-primary" onclick="handleClick(1)">Short</a>
  <button type="button" class="btn btn-primary" onclick="handleClick(2)">Medium</a>
  <button type="button" class="btn btn-primary" onclick="handleClick(3)">Long</a>
</div>
```

`onclick` calls `handleClicks` found in *project/static/main.js*, which sends an AJAX POST requests to the server with the appropriate task type: `1`, `2`, or `3`.

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

On the server-side, a route is already configured to handle the request in *project/main.py*

```py
@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    return JSONResponse(task_type)
```