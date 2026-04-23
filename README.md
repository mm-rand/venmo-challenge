# Running project

requires uv, just, docker

```bash
just start-infrastructure
just develop
```

# Requests

create project:
```bash
curl -i -X POST http://localhost:8000/projects/ \
  -H "x-api-key: some-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "My project Description"}'
```

get project:
```bash
curl -i -X GET http://localhost:8000/projects/<PROJ_ID> \
  -H "x-api-key: some-api-key"
```

update project:
```bash
curl -i -X PUT http://localhost:8000/projects/<PROJ_ID> \
  -H "x-api-key: some-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "description": "Updated Description"}'
```

delete project:
```bash
curl -i -X DELETE http://localhost:8000/projects/<PROJ_ID> \
  -H "x-api-key: some-api-key"
```

create high priority task:
```bash
curl -i -X POST http://localhost:8000/projects/<PROJ_ID>/tasks/ \
  -H "x-api-key: some-api-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "High Priority", "priority": 10}'
```

create low priority task:
```bash
curl -i -X POST http://localhost:8000/projects/<PROJ_ID>/tasks/ \
  -H "x-api-key: some-api-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "Low Priority", "priority": 1}'
```

list sorting by priority:
```bash
curl -i -X GET "http://localhost:8000/projects/<PROJ_ID>/tasks/?limit=10&offset=0" \
  -H "x-api-key: some-api-key"
```

update task:
```bash
curl -i -X PUT http://localhost:8000/tasks/<TASK_ID> \
  -H "x-api-key: some-api-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "priority": 5, "completed": true}'
```

delete task:
```bash
curl -i -X DELETE http://localhost:8000/tasks/<TASK_ID> \
  -H "x-api-key: some-api-key"
```
