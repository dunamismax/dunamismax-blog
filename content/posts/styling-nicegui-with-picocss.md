---
title: Styling NiceGUI with Pico.css
date: 8/2/2025
time: 03:03
summary: Enhance NiceGUI interfaces with Pico.css, global CSS variables, and component
  classes.
tags:
- nicegui
- css
- pico
- styling
- tutorial
---

# Styling NiceGUI with Pico.css

Pico.css provides a clean, minimal look that pairs well with NiceGUI. By mixing Pico's semantic classes with NiceGUI components you get a modern dark theme without writing verbose CSS. Pico favors native HTML elements and a small stylesheet, so pages load quickly and remain accessible.

The framework exposes a handful of CSS variables for easy theming. Adjusting colors or fonts requires only a few overrides, and NiceGUI's `ui.add_head_html` makes it simple to include the stylesheet once at startup.

## Adding Pico.css

```python
from nicegui import ui

ui.add_head_html(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">'
)
```

For offline builds, download the file and serve it from `static/`. You can even pin a specific version to ensure reproducible styles across deployments.

## Component Classes

NiceGUI exposes a `classes` helper to append Pico classes:

```python
with ui.row().classes('grid'):
    ui.button('Primary').classes('primary')
    ui.button('Outline').classes('outline')
```

The helper works on all components. Add `ui.input('Email').classes('input')` for form fields or apply `classes('contrast')` to emphasize alerts.

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

Define additional variables such as `--h1-color` or `--button-border-radius` to fine‑tune the look. Keep overrides scoped to avoid unintended side effects.

## Custom Fonts

Load Google Fonts or local fonts with another `ui.add_head_html` call:

```python
ui.add_head_html('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap">')
```

Reference the font in `blog.css` using `font-family: "Inter", sans-serif;` to keep typography consistent.

## Responsive Layouts

Combine Pico's grid with NiceGUI rows and columns to support phones and tablets. Use media queries in `blog.css` to tweak padding or font sizes for smaller screens.

Import the stylesheet once and enjoy consistent styling across pages.

