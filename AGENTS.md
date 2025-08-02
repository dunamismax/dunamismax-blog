# Project Instructions for NiceGUI Dark Blog

## Overview
- **Project**: NiceGUI Dark Blog
- **Version**: 1.0.0
- **Theme**: dark layout with purple accents
- **Architecture**: file-based content, no database, standalone executable

## Technology Stack
- Python 3.13+
- NiceGUI 2.22.1+
- Markdown with `python-frontmatter`, `pymdown-extensions`, `pygments`
- Pico.css with custom overrides
- Cachetools TTLCache
- uv for dependency management
- Ruff for formatting and linting
- PyInstaller for builds

## Repository Layout
```
app/        # NiceGUI application code
content/    # Markdown posts with YAML frontmatter
static/     # CSS and other static assets
tests/      # Pytest test suite
build.py    # PyInstaller build script
pyproject.toml
```

## Coding Conventions
- Run `uv run ruff format .` and `uv run ruff check . --fix` after edits
- Use full Python 3.13 type hints and meaningful docstrings
- Apply `@ui.refreshable` for dynamic UI sections
- Enable dark mode with `ui.dark_mode().enable()`
- Add styles via `ui.add_head_html()` instead of inline CSS
- Organize routes with `@ui.page` functions and keep components reusable
- Keep global styles in `static/blog.css` and other files under `static/`

## Testing & Quality
- Use pytest for all tests
- For substantial features, write failing tests before implementation
- Never fake or skip tests to force success
- Include logging and graceful error handling
- Maintain performance targets: cached pages should respond in <100 ms

## Commands
```bash
uv run python app/main.py      # run development server
uv run ruff format .
uv run ruff check . --fix
uv run pytest
uv run python build.py         # build executable
```

## Content Format
Markdown posts use YAML frontmatter:
```yaml
---
title: "Post Title"
date: "8/1/2025"
summary: "Brief description"
tags: ["tag1", "tag2"]
---

# Markdown content
```

## Important Notes
- Commit on the `main` branch and open a pull request for every change
- Configure git user as `dunamismax <dunamismax@tutamail.com>`
- Clean up or merge obsolete branches that are not `main`
- Append `2025` to every web search query
- Keep PR messages concise, free of tags, and authored as `dunamismax`
- Write modern, pythonic code; avoid emojis and em dashes
- Do not mention Codex or this chat in commits or PRs
- Maintain the dark theme colors `#713A90` and `#1E1E2E`

