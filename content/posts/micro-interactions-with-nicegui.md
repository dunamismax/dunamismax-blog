---
title: "Tiny Touches: Micro-Interactions in NiceGUI"
date: "8/8/2025"
summary: "Add playful animations and feedback to make your NiceGUI apps feel alive."
tags: ["nicegui", "ui", "animations", "tips"]
---

# Tiny Touches: Micro-Interactions in NiceGUI

Small animations and responsive feedback can turn a plain interface into an engaging experience. NiceGUI's declarative API makes it easy to sprinkle micro-interactions throughout your app.

## Animated Counters

Use `@ui.refreshable` to update elements smoothly when state changes:

```python
from nicegui import ui

count = 0

@ui.refreshable
def counter() -> None:
    ui.label(f'Clicks: {count}').classes('transition-all')

@ui.page('/counter')
def show_counter() -> None:
    counter()
    ui.button('Click me', on_click=lambda: (globals().__setitem__('count', count + 1), counter.refresh()))
```

The label fades between values thanks to the `transition-all` class.

## Notifying Actions

Micro-feedback keeps users informed. A simple call to `ui.notify` can confirm that an action succeeded:

```python
ui.button('Save', on_click=lambda: ui.notify('Saved!', type='positive'))
```

## Delight Through Detail

These tiny touches make a big impression. Experiment with classes like `animate-bounce` or subtle color shifts to give your NiceGUI interfaces personality.
