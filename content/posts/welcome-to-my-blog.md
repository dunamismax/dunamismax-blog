---
title: "Welcome to My Blog"
date: "2024-01-15"
summary: "This is the first post on my new blog built with NiceGUI. Learn about the features and capabilities of this file-based blogging system."
---

# Welcome to My Blog!

Welcome to my new blog! This is a demonstration of a file-based blog built with **NiceGUI**, **Pico.css**, and Python.

## Features

This blog template includes several powerful features:

- 📝 **File-based content management** - Simply add `.md` files to the `content/posts` directory
- 🎨 **Clean, responsive design** with Pico.css
- 🖥️ **Syntax highlighting** for code blocks using Pygments
- 📱 **Mobile-friendly** responsive layout
- ⚡ **Fast and lightweight** - pure Python stack with NiceGUI

## Code Example

Here's a simple Python function with syntax highlighting:

```python
def greet(name: str) -> str:
    """Generate a friendly greeting."""
    return f"Hello, {name}! Welcome to the blog."

# Example usage
message = greet("World")
print(message)
```

## Markdown Support

The blog supports all standard Markdown features plus some extensions:

- **Bold** and *italic* text
- [Links](https://nicegui.io)
- Lists (like this one!)
- Code blocks with syntax highlighting
- Tables
- Task lists
- And much more!

## Getting Started

To add your own posts:

1. Create a new `.md` file in the `content/posts` directory
2. Add YAML frontmatter with `title`, `date`, and `summary`
3. Write your content in Markdown below the frontmatter
4. The blog will automatically display your new post!

That's it! Enjoy blogging with NiceGUI. 🎉