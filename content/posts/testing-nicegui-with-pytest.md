---
title: 'Bulletproof NiceGUI: Testing with Pytest'
date: 8/2/2025
time: 03:11
summary: Learn how to verify your NiceGUI pages and utilities using pytest and a few
  handy helpers.
tags:
- nicegui
- pytest
- testing
- python
---

# Bulletproof NiceGUI: Testing with Pytest

Adding tests to a NiceGUI project keeps the UI reliable as it grows. This blog uses **pytest** to exercise content helpers and to catch rendering bugs before they ship.

## Getting Started

Install dependencies and run the suite with a single command:

```bash
uv run pytest
```

Pytest discovers tests in the `tests/` folder. For example, `test_content.py` checks that slugs are generated correctly and that Markdown files load with word counts.

## Testing Components

You can also test UI functions directly. NiceGUI pages are regular Python functions, so they fit neatly into the pytest workflow:

```python
from nicegui import ui

@ui.page('/hello')
def hello() -> None:
    ui.label('hi')

def test_page_registration() -> None:
    assert '/hello' in ui.app.routes
```

This pattern verifies that a route exists without spinning up a server.

## Continuous Confidence

Automated tests free you to refactor boldly. Whether you're adding new widgets or changing markdown parsing, a quick `uv run pytest` confirms everything still works.

