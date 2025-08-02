---
title: "Building Modern Web Apps with NiceGUI v2.22.1"
date: "8/1/2025"
summary: "Learn how NiceGUI lets you craft full-featured web apps in pure Python."
tags: ["nicegui", "python", "web-development", "ui", "framework", "tutorial"]
---

# Building Web Apps with NiceGUI

[NiceGUI](https://nicegui.io) enables developers to create web applications entirely in Python. No HTML, CSS, or JavaScript is required.

## Why NiceGUI?

- **Pure Python** – write UI and backend logic with the same language.
- **Rapid development** – prototype quickly without context switching.
- **Rich components** – buttons, inputs, charts, and more included out of the box.

## Basic Components

```python
from nicegui import ui

ui.label('Hello, World!')
ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
ui.input('Enter text here')
ui.slider(min=0, max=100, value=50)
```

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

## Ideal Use Cases

- Dashboards and admin interfaces
- Prototypes and MVPs
- Internal tools
- Data visualization
- IoT control panels

## Conclusion

NiceGUI lowers the barrier to building modern, interactive web applications. Give it a try for your next project!
