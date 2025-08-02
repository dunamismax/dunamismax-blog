---
title: "Deploying NiceGUI with Docker"
date: "8/1/2025"
summary: "Package and run NiceGUI applications in lightweight Docker containers."
tags: ["nicegui", "docker", "deployment", "tutorial"]
---

# Deploying NiceGUI with Docker

Containerizing a NiceGUI app ensures consistent environments from development to production.

## Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir uv && uv pip install .

CMD ["uv", "run", "python", "app/main.py"]
```

## Build and Run

```bash
docker build -t nicegui-app .
docker run -p 8080:8080 nicegui-app
```

Your application is now accessible at `http://localhost:8080`.
