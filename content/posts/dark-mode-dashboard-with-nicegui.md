---
title: "Designing a Dark Mode Dashboard with NiceGUI"
date: "8/1/2025"
summary: "Create a sleek dark-themed dashboard using NiceGUI and Pico.css."
tags: ["nicegui", "dashboard", "dark-mode", "ui", "tutorial"]
---

# Designing a Dark Mode Dashboard

NiceGUI makes it simple to build dashboards that look great in dark mode.

## Enabling Dark Mode

```python
from nicegui import ui

ui.dark_mode().enable()
```

## Sample Layout

```python
from nicegui import ui

@ui.page('/')
def dashboard():
    ui.dark_mode().enable()
    with ui.row():
        ui.card().with_content(ui.label('CPU: 42%'))
        ui.card().with_content(ui.label('RAM: 3.2 GB'))
    ui.button('Refresh', on_click=lambda: ui.notify('Data refreshed'))
```

Customize styles in `static/blog.css` to match your brand colors.
