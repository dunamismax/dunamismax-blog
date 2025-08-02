---
title: Deploying NiceGUI with Docker
date: 8/2/2025
time: 14:40
summary: Package and run NiceGUI applications in lightweight Docker containers using
  modern Python tooling.
tags:
- nicegui
- docker
- deployment
- tutorial
---

# Deploying NiceGUI with Docker

Containerizing a NiceGUI app ensures consistent environments from development to production. Docker images bundle Python, NiceGUI, and your code so the application runs the same on any host. Shipping an image means you can deploy to any platform that supports Docker without worrying about missing dependencies or incompatible Python versions.

A minimal image reduces attack surface and download size. Start with `python:3.13-slim` and add only the files and tools you need. Use a `.dockerignore` file to exclude tests and development artifacts so the build context stays small.

## Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir uv && uv pip install .

CMD ["uv", "run", "python", "app/main.py"]
```

This single-stage file copies the source and installs dependencies via `uv`. For leaner images consider a multi-stage build:

```dockerfile
FROM python:3.13-slim AS builder
WORKDIR /build
COPY . .
RUN pip install --no-cache-dir uv && uv pip install .

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /build /app
CMD ["uv", "run", "python", "app/main.py"]
```

The builder stage compiles wheels and keeps build tools out of the final image. You can also install system packages or run tests in the builder stage before producing the runtime layer.

## Build and Run

```bash
docker build -t nicegui-app .
docker run -p 8080:8080 nicegui-app
```

Use environment variables to configure runtime settings:

```bash
docker run -e PORT=8080 -p 8080:8080 nicegui-app
```

Inside `app/main.py` read `os.environ['PORT']` to customize the server port.

Mounting a volume with `-v $(pwd)/content:/app/content` lets you update Markdown posts without rebuilding the image. For production deployments, add a `HEALTHCHECK` directive so orchestrators like Docker Swarm can restart unhealthy containers automatically.

## Docker Compose

For multi-service deployments define a `docker-compose.yml` file:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      PORT: 8080
```

Running `docker compose up` builds and starts the container. Your application is now accessible at `http://localhost:8080`.

Compose files also support named volumes, secrets, and multiple services. You could add a reverse proxy, database, or background worker and manage them all with a single command.

## Conclusion

Docker packages your NiceGUI app with everything it needs, simplifying deployment to cloud providers or on-prem servers. Pair it with `TTLCache` for snappy performance and you'll have a portable, fast, dark-themed web interface. With a solid container strategy, you can roll out updates confidently and keep environments in sync across your team.
