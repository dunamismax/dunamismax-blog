---
title: "Designing a Dark Mode Dashboard with NiceGUI"
date: "8/1/2025"
summary: "Create a sleek dark-themed dashboard using NiceGUI, Pico.css, and Python." 
tags: ["nicegui", "dashboard", "dark-mode", "ui", "tutorial"]
---

# Designing a Dark Mode Dashboard

NiceGUI makes it simple to build dashboards that look great in dark mode. With a single call you can enable a `#1E1E2E` background that is easy on the eyes in low‑light settings. Pico.css ensures typography and spacing feel polished without writing custom CSS.

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

Group metrics in `ui.card` containers for a clean layout. For more complex dashboards, wrap charts with `@ui.refreshable` so clicking the refresh button updates data in place without reloading the page.

## Adding Charts

```python
from nicegui import ui
import random

@ui.page('/metrics')
def metrics() -> None:
    ui.dark_mode().enable()
    @ui.refreshable
    def chart() -> None:
        values = [random.randint(0, 100) for _ in range(5)]
        ui.line_plot(values)

    chart()
    ui.button('Update', on_click=chart.refresh)
```

## Custom Styling

Adjust colors and spacing through `static/blog.css` to match your brand. Setting `--primary: #713A90;` preserves the purple accent used throughout this site.

## Responsive Design

Wrap rows in `ui.column()` on narrow screens so widgets stack vertically. Using percentage-based widths or Flexbox classes keeps the layout usable on phones and tablets.

## Conclusion

With dark mode enabled and Pico.css handling baseline styles, you can focus on the data that matters. NiceGUI's Pythonic approach lets you experiment quickly and deliver dashboards that look sharp day or night.
