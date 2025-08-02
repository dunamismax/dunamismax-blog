---
title: "Styling NiceGUI with Pico.css"
date: "8/1/2025"
summary: "Enhance NiceGUI interfaces with Pico.css and custom styles."
tags: ["nicegui", "css", "pico", "styling", "tutorial"]
---

# Styling NiceGUI with Pico.css

Pico.css provides a clean, minimal look that pairs well with NiceGUI.

## Adding Pico.css

```python
from nicegui import ui

ui.add_head_html(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">'
)
```

## Custom Styles

Place custom overrides in `static/blog.css`:

```css
:root {
    --primary: #713A90;
    --background-color: #1E1E2E;
}
```

Import the stylesheet once and enjoy consistent styling across pages.
