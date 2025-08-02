---
title: 'Under the Hood: Powering the NiceGUI Blog'
date: 8/2/2025
time: 03:12
summary: Explore the full stack—from Python and NiceGUI to caching, styling, and build
  tools—that keeps this blog humming.
tags:
- nicegui
- tech-stack
- python
- blog
---

# Under the Hood: Powering the NiceGUI Blog

Every page on this site flows from a lean stack designed for clarity and speed. The core is **Python 3.13** running **NiceGUI 2.22.1** on top of **FastAPI**. Content lives in Markdown files with YAML front matter, parsed by `python-frontmatter` and rendered with `markdown` and `pymdown-extensions`.

## Styling the UI

The dark theme uses `#1E1E2E` for backgrounds and a purple accent of `#713A90`. Lightweight **Pico.css** provides a responsive base, while custom rules in `static/blog.css` polish the layout.

## Keeping Things Fast

`cachetools.TTLCache` keeps recent posts and rendered HTML in memory:

```python
from cachetools import TTLCache

posts_cache = TTLCache(maxsize=100, ttl=600)
```

Caching ensures that repeat visits load in under a blink.

## Tooling and Distribution

Dependencies are managed with **uv**, and code quality stays sharp thanks to **Ruff**. When it is time to ship, **PyInstaller** bundles everything into a standalone executable.

## Putting It All Together

This combination of modern Python tooling and a minimalist UI framework makes the blog quick to maintain and easy to extend. Drop a Markdown file into `content/posts`, run `uv run python app/main.py`, and the stack does the rest.

