---
title: "Building Modern Web Apps with NiceGUI v2.22.1"
date: "8/1/2025"
summary: "Discover the latest features in NiceGUI v2.22.1 for building lightning-fast web applications entirely in Python. Featuring modern components, caching, and performance optimizations!"
tags: ["nicegui", "python", "web-development", "ui", "framework", "tutorial"]
---

# Building Web Apps with NiceGUI

[NiceGUI](https://nicegui.io) is a revolutionary Python framework that allows you to build web applications using only Python. No need to write HTML, CSS, or JavaScript!

## Why NiceGUI?

NiceGUI offers several compelling advantages:

### Pure Python
Write your entire application in Python, including the UI logic and styling.

### Rapid Development
Build interactive web apps quickly without context switching between languages.

### Batteries Included
Comes with a rich set of UI components out of the box.

## Key Components

NiceGUI provides many useful components:

```python
from nicegui import ui

# Create various UI elements
ui.label('Hello World!')
ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
ui.input('Enter text here')
ui.slider(min=0, max=100, value=50)
```

## Styling with CSS Frameworks

NiceGUI works great with CSS frameworks like Pico.css:

```python
# Add external stylesheets
ui.add_head_html('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">')

# Apply CSS classes
ui.button('Styled Button').classes('secondary')
```

## Routing

NiceGUI makes routing simple with decorators:

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

One of NiceGUI's strengths is real-time updates:

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

## Perfect for Prototyping

NiceGUI is excellent for:

- **Dashboards** and admin interfaces
- **Prototypes** and MVPs
- **Internal tools** and utilities
- **Data visualization** applications
- **IoT interfaces** and control panels

## Conclusion

NiceGUI opens up web development to Python developers who want to stay in their comfort zone while building modern, interactive web applications. Give it a try for your next project!

---

*Want to learn more? Check out the [official NiceGUI documentation](https://nicegui.io/documentation) for comprehensive guides and examples.*