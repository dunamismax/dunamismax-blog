---
title: "Styling NiceGUI with Pico.css"
date: "8/1/2025"
summary: "Enhance NiceGUI interfaces with Pico.css, global CSS variables, and component classes." 
tags: ["nicegui", "css", "pico", "styling", "tutorial"]
---

# Styling NiceGUI with Pico.css

Pico.css provides a clean, minimal look that pairs well with NiceGUI. By mixing Pico's semantic classes with NiceGUI components you get a modern dark theme without writing verbose CSS.

## Adding Pico.css

```python
from nicegui import ui

ui.add_head_html(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">'
)
```

## Component Classes

NiceGUI exposes a `classes` helper to append Pico classes:

```python
with ui.row().classes('grid'):
    ui.button('Primary').classes('primary')
    ui.button('Outline').classes('outline')
```

## Custom Styles

Place overrides in `static/blog.css` and adjust global variables:

```css
:root {
    --primary: #713A90;
    --background-color: #1E1E2E;
    --font-size: 16px;
}

button.outline {
    border-color: var(--primary);
}
```

## Responsive Layouts

Combine Pico's grid with NiceGUI rows and columns to support phones and tablets. Use media queries in `blog.css` to tweak padding or font sizes for smaller screens.

Import the stylesheet once and enjoy consistent styling across pages.
