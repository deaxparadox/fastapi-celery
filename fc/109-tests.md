# Tests

Let's start with the most basic test:

```py
def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)
```

Add the above test case to *project/tests/test_tasks.py*, and then add the following import:

```py
from worker import create_task
```

Run that test individually:

```bash
$ docker compose exec web python -m pytest -k "test_task and not test_home"
```

It should tak about one minute to run:

```bash
$ docker compose exec web pytest
======================================== test session starts =========================================
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.4.0
rootdir: /usr/src/app
plugins: anyio-4.2.0
collected 2 items                                                                                    

tests/test_tasks.py ..                                                                         [100%]

==================================== 2 passed in 60.06s (0:01:00) ====================================
```

It's worth noting that in the above asserts, we used the `.run` method (rather then `.delay`) to run the task directly without a Celery worker.

Wantt to mock the `.run` method to speed things up?

```py
@patch("worker.create_task.run")
def test_mock_task(mock_run):
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    assert create_task.run(2)
    assert create_task.run.call_count == 2

    assert create_task.run(3)
    assert create_task.run.call_count == 3
```

import:

```py
from unittest.mock import path
```

Test:

```bash
$ docker compose exec web pytest -k 'test_mock_task' -vv
======================================== test session starts =========================================
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.4.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /usr/src/app
plugins: anyio-4.2.0
collected 3 items / 2 deselected / 1 selected                                                        

tests/test_tasks.py::test_mock_task PASSED                                                     [100%]

================================== 1 passed, 2 deselected in 0.03s ===================================
```

----------


Full Integration test?

```py
def test_task_status(test_app):
    response = test_app.post(
        "/tasks",
        data=json.dumps({"type": 1})
    )
    content = response.json()
    task_id = content["task_id"]
    assert task_id

    response = test_app.get(f"tasks/{task_id}")
    content = response.json()
    assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
    assert response.status_code == 200

    while content["task_status"] == "PENDING":
        response = test_app.get(f"tasks/{task_id}")
        content = response.json()
    assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}
```

Keep in mind that this test uses the same broker and backend used in development. You may want to instantiate a new Celery app for testing.


Add the import:

```py
import json
```