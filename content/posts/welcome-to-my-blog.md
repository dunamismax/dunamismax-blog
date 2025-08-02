---
title: "Welcome to My Modern NiceGUI Blog"
date: "8/1/2025"
summary: "An introduction to a lightning-fast NiceGUI blog built with a dark theme, caching, and modern Python tooling." 
tags: ["nicegui", "python", "web-development", "blog", "tutorial"]
---

# Welcome

This site showcases a file-based blog powered by **NiceGUI v2.22.1**, **Pico.css**, and **Python 3.13**. Posts are stored as Markdown files and rendered on the fly with caching for snappy navigation. The dark theme uses `#1E1E2E` and `#713A90` to provide a consistent look across pages.

## Features

- File-based content management
- Responsive design tuned for dark mode
- Syntax-highlighted code blocks
- Fast page loads thanks to caching
- Search and tagging for quick discovery
- Blog statistics and reading time estimates

## Under the Hood

Every post includes YAML front matter for metadata. The NiceGUI app scans the `content/posts` directory at startup and serves each file as an individual page. `cachetools.TTLCache` keeps rendered Markdown in memory for 60 seconds, ensuring quick navigation while still picking up edits.

## Code Example

```python
def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}! Welcome to the blog."

message = greet("World")
print(message)
```

## Get Started

1. Drop a `.md` file into `content/posts`.
2. Add YAML front matter with `title`, `date`, and `summary`.
3. Write your post in Markdown.
4. Refresh the browser to see it appear instantly.

## Running Locally

To hack on the blog, install dependencies with `uv pip install -r requirements.txt` (handled automatically via the lockfile) and start the dev server:

```bash
uv run python app/main.py
```

Open `http://localhost:8080` in your browser and you'll see the blog in action. Make a change to a Markdown file and the page updates after a refresh thanks to file-based routing.

Enjoy exploring NiceGUI and happy blogging!
