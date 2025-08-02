---
title: "Building Modern Web Apps with NiceGUI v2.22.1"
date: "8/15/2025"
summary: "A tour of NiceGUI's Python-centric approach to building feature-rich web applications without touching JavaScript."
tags: ["nicegui", "python", "web-development", "ui", "framework", "tutorial"]
---

# Building Web Apps with NiceGUI

[NiceGUI](https://nicegui.io) enables developers to create web applications entirely in Python. It sits atop FastAPI and Vue.js yet hides that complexity so you can stay focused on business logic. The framework ships with a dark theme out of the box and a component library that covers most dashboard use cases.

NiceGUI applications start a regular FastAPI server and attach Vue components on the client. Because it runs in a single Python process you can share variables between routes, schedule background tasks with asyncio, or integrate directly with existing FastAPI routers. This tight coupling keeps your mental model small and avoids context switching to JavaScript for interactivity.

## Why NiceGUI?

- **Pure Python** – author UI and backend logic with the same language, keeping your stack consistent.
- **Rapid development** – hot-reload and a declarative API let you prototype ideas in minutes.
- **Rich components** – buttons, charts, tables, dialogs, and file pickers are ready to use.
- **Dark mode first** – enable a polished `#1E1E2E` background with purple accents via `ui.dark_mode().enable()`.
- **Works with FastAPI** – mount routers or reuse dependency injections when you need REST endpoints.
- **Server-push updates** – refresh widgets from background jobs or WebSocket events without polling.
- **Lightweight deployment** – ship apps as a PyInstaller binary or container image without extra build steps.

## Basic Components

```python
from nicegui import ui

ui.label('Hello, World!')
ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
ui.input('Enter text here')
ui.slider(min=0, max=100, value=50)
with ui.row():
    ui.checkbox('Accept terms')
    ui.switch('Dark mode')
```

Layout primitives like `ui.row()` and `ui.column()` make it easy to build responsive UIs without writing CSS. Components can be refreshed dynamically by wrapping them with `@ui.refreshable` decorators.

For more advanced layouts, combine rows and columns inside `ui.card()` containers or create reusable functions that compose widgets. NiceGUI mirrors Vue's component model, allowing you to pass callbacks and references to nested layouts.

## Styling with Pico.css

```python
ui.add_head_html(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">'
)
ui.button('Styled Button').classes('secondary')
```

## Routing

```python
@ui.page('/')
def index():
    ui.label('Home Page')

@ui.page('/about')
def about():
    ui.label('About Page')

@ui.page('/blog/{slug}')
def blog_post(slug: str):
    ui.label(f'Blog Post: {slug}')
```

Routes can also return data or mount subpages. Because NiceGUI runs on top of FastAPI, you can declare dependencies or background tasks as you would in any FastAPI project.

To keep navigation snappy, consider preloading common pages and caching expensive computations. Use `cachetools.TTLCache` to store rendered markdown or API responses and invalidate the cache when content changes.

## Real-time Updates

```python
import asyncio
from datetime import datetime

@ui.page('/clock')
def clock():
    label = ui.label()

    async def update_time():
        while True:
            label.text = datetime.now().strftime('%H:%M:%S')
            await asyncio.sleep(1)

    ui.timer(1.0, update_time)
```

Asynchronous components like timers keep pages reactive. Combine them with `asyncio.create_task` to update charts or tables in the background while the user interacts with the page.

Real‑time features extend beyond clocks. You can push sensor readings, chat messages, or stock prices by scheduling coroutines that modify component properties. NiceGUI handles the WebSocket communication behind the scenes.

## Forms and State

Input elements share state through Python variables. You can easily validate fields or compute derived values:

```python
name = ui.input('Name')
age = ui.number('Age', value=0)

def submit() -> None:
    ui.notify(f"Registered {name.value} who is {age.value} years old")

ui.button('Register', on_click=submit)
```

You can also bind widgets to dataclasses or Pydantic models. Persist user preferences in a dictionary and call `ui.context.client.storage` to save settings in the browser for the next visit.

## Working with Backend APIs

Because NiceGUI reuses FastAPI's dependency system, external services are just function calls away. Define a service layer that fetches data or performs mutations and invoke it from UI callbacks. Responses can populate tables or trigger notifications. For multi‑user apps, secure routes with OAuth2 and use `ui.open` to redirect to login pages.

## Deployment Options

For quick experiments run `uv run python app/main.py`. When it is time to share your app, package it with Docker or PyInstaller. A container ensures that the dark-themed interface and dependencies are consistent across environments.

PyInstaller bundles the interpreter and your code into a single executable that runs on machines without Python installed. For Docker deployments, expose the port with `-p 8080:8080` and rely on environment variables for configuration. Regardless of the method, remember to serve static files through a reverse proxy like Caddy or Nginx for better caching.

## Ideal Use Cases

- Dashboards and admin interfaces
- Prototypes and MVPs
- Internal tools
- Data visualization
- IoT control panels

## Conclusion

NiceGUI lowers the barrier to building modern, interactive web applications. With dark mode support, a Pythonic API, and seamless integration with FastAPI, it is a compelling choice for dashboards, internal tools, and prototypes. With thoughtful state management and a straightforward deployment story, NiceGUI helps teams deliver polished interfaces quickly. Give it a try for your next project and see how far pure Python can take you.
