---
title: "Designing a Dark Mode Dashboard with NiceGUI"
date: "8/10/2025"
summary: "Create a sleek dark-themed dashboard using NiceGUI, Pico.css, and Python." 
tags: ["nicegui", "dashboard", "dark-mode", "ui", "tutorial"]
---

# Designing a Dark Mode Dashboard

NiceGUI makes it simple to build dashboards that look great in dark mode. With a single call you can enable a `#1E1E2E` background that is easy on the eyes in low‑light settings. Pico.css ensures typography and spacing feel polished without writing custom CSS. A dark palette reduces glare, highlights data visualizations, and matches the purple accent color defined in this project's theme.

Well‑structured dashboards surface critical metrics while keeping controls intuitive. NiceGUI's declarative API lets you experiment quickly, mixing layout primitives and interactive widgets until the page feels right.

## Enabling Dark Mode

```python
from nicegui import ui

ui.dark_mode().enable()
```

To remember a user's preference, store the choice in `ui.context.client.storage` and toggle dark mode based on that value during page load.

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

You can also nest rows and columns to create responsive grids. Icons from libraries like [Tabler Icons](https://tabler.io/icons) convey status at a glance. Calling `ui.notify` after actions gives users immediate feedback.

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

For streaming data, pair charts with `ui.timer` to refresh automatically every few seconds. Timers keep the page reactive without forcing full refreshes.

## Custom Styling

Adjust colors and spacing through `static/blog.css` to match your brand. Setting `--primary: #713A90;` preserves the purple accent used throughout this site.

If you need per‑widget tweaks, append Pico classes using `classes('outline')` or add a custom CSS file. Keep overrides minimal so future framework updates remain painless.

## Responsive Design

Wrap rows in `ui.column()` on narrow screens so widgets stack vertically. Using percentage-based widths or Flexbox classes keeps the layout usable on phones and tablets.

Test layouts across multiple viewports and use media queries in `blog.css` to adjust padding and font sizes. Small touches like larger tap targets improve usability on touch devices.

## Conclusion

With dark mode enabled and Pico.css handling baseline styles, you can focus on the data that matters. NiceGUI's Pythonic approach lets you experiment quickly and deliver dashboards that look sharp day or night. Thoughtful persistence and live updates turn a static dashboard into a dynamic tool your team will rely on.
