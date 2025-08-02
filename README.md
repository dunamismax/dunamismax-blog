<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/NiceBlog.png" alt="NiceGUI Blog" width="300" />
</p>

<p align="center">
  <a href="https://github.com/dunamismax/nicegui-blog">
    <img src="https://readme-typing-svg.demolab.com/?font=Inter&weight=600&size=26&pause=800&color=713A90&center=true&vCenter=true&width=1200&height=80&lines=Dark+Theme+NiceGUI+Blog+Application;Python+3.13+%2B+NiceGUI+2.22.1;Purple+%26+Orange+Aesthetic+Design;Lightning+Fast+TTL+Cached+Content;Real+Time+Search+%26+Pagination;Image+Optimization+%26+Lazy+Loading;File+Based+Content+Management;Zero+Database+Dependencies;Standalone+Executable+Distribution;MIT+Licensed+Open+Source" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3130/"><img src="https://img.shields.io/badge/Python-3.13+-713A90.svg?logo=python&logoColor=white&style=for-the-badge" alt="Python Version"></a>
  <a href="https://nicegui.io/"><img src="https://img.shields.io/badge/NiceGUI-v2.22.1-713A90.svg?logo=fastapi&logoColor=white&style=for-the-badge" alt="NiceGUI Version"></a>
  <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/uv-Package_Manager-713A90.svg?style=for-the-badge" alt="uv Package Manager"></a>
  <a href="https://pyinstaller.org/"><img src="https://img.shields.io/badge/PyInstaller-v6.14.2-713A90.svg?style=for-the-badge" alt="PyInstaller"></a>
</p>

<p align="center">
  <a href="https://docs.astral.sh/ruff/"><img src="https://img.shields.io/badge/Ruff-Formatted-713A90.svg?style=for-the-badge" alt="Ruff Formatting"></a>
  <a href="https://pygments.org/"><img src="https://img.shields.io/badge/Pygments-Dark_Theme-713A90.svg?style=for-the-badge" alt="Pygments"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-713A90.svg?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Theme-Dark_Mode-713A90.svg?style=for-the-badge" alt="Dark Theme">
</p>

---

<div align="center">

# NiceGUI Blog

<p style="color: #713A90; font-size: 18px; font-weight: 500;">
A stunning dark-themed blog application built with Python 3.13 and NiceGUI v2.22.1<br>
Featuring beautiful purple & orange aesthetics with lightning-fast performance
</p>

</div>

## Core Features

<table align="center">
<tr>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-Python_3.13-713A90?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13"><br>
<sub><b>Latest Python Performance</b></sub>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-Dark_Theme-713A90?style=for-the-badge&logo=moon&logoColor=white" alt="Dark Theme"><br>
<sub><b>Beautiful Dark UI</b></sub>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-File_Based-713A90?style=for-the-badge&logo=markdown&logoColor=white" alt="File Based"><br>
<sub><b>Zero Database Dependencies</b></sub>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-Standalone-713A90?style=for-the-badge&logo=package&logoColor=white" alt="Standalone"><br>
<sub><b>Single Executable</b></sub>
</td>
</tr>
</table>

* **Enhanced Search & Pagination**: Real-time search with smart pagination (5 posts per page)
* **Image Optimization**: Lazy loading, responsive images with hover effects
* **Modern Header Design**: Gradient background, feature badges, improved typography
* **Comprehensive Favicon Support**: All device formats with proper meta tags
* **Advanced Styling**: Custom scrollbars, smooth animations, enhanced hover effects
* **Built-in HTML sanitization** to prevent XSS
* **Token-protected admin cache management** endpoint

## Project Structure

```sh
nicegui-blog/
├── app/                      # Application source
│   ├── main.py              # NiceGUI application with modern UI patterns
│   └── content.py           # Robust content loading with error handling
├── content/                 # Blog content
│   └── posts/               # Markdown blog posts with front matter
├── static/                  # Static assets
│   ├── blog.css            # Global styles with modern enhancements
│   ├── syntax.css          # Auto-generated Pygments styling
│   └── favicon/            # Comprehensive favicon collection
├── tests/                   # Test suite
├── build.py                 # PyInstaller build script
└── pyproject.toml           # Modern Python project configuration
```

---

<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/Repo-Features.png" alt="Repository Features" width="300" />
</p>

## Quick Start

**Prerequisites:** Python 3.13+ and uv package manager

```bash
# Install uv package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the repository
git clone https://github.com/dunamismax/nicegui-blog.git
cd nicegui-blog

# Setup Python 3.13 environment and dependencies
uv python install 3.13
uv python pin 3.13
uv sync

# Set admin token for cache route
export BLOG_ADMIN_TOKEN=your-token

# Run code quality checks and tests
uv run ruff format .
uv run ruff check . --fix
uv run pytest

# Run the application in development mode
uv run python app/main.py
```

<div align="center">

**Application available at** `http://localhost:8080`

<img src="https://img.shields.io/badge/Status-Ready_to_Run-713A90?style=for-the-badge" alt="Ready">
<img src="https://img.shields.io/badge/Performance-Lightning_Fast-713A90?style=for-the-badge" alt="Fast">

</div>

### Available Routes

<table>
<tr>
<td><code>/blog</code></td>
<td>Main blog index with modern header, search, pagination, and statistics</td>
<td><img src="https://img.shields.io/badge/-Main-713A90?style=flat" alt="Main"></td>
</tr>
<tr>
<td><code>/blog/&lt;slug&gt;</code></td>
<td>Individual blog posts with beautiful typography</td>
<td><img src="https://img.shields.io/badge/-Posts-713A90?style=flat" alt="Posts"></td>
</tr>
<tr>
<td><code>/admin/cache?token=&lt;token&gt;</code></td>
<td>Token-protected cache management interface</td>
<td><img src="https://img.shields.io/badge/-Admin-713A90?style=flat" alt="Admin"></td>
</tr>
</table>

---

## Content Management

### Creating Blog Posts

```markdown
---
title: "Your Post Title"
date: "8/1/2025"
summary: "Brief description for the blog index"
---

# Your Content Here

Full markdown support with:
- Syntax highlighting
- Tables and task lists
- Math expressions
- Custom fences and diagrams
```

### Enhanced Content Features

* **Multi-Format Dates**: ISO, YYYY-MM-DD, natural language formats
* **Advanced Markdown**: Tables, task lists, syntax highlighting, TOC generation
* **Image Optimization**: Automatic lazy loading, responsive scaling, hover effects
* **Auto-Generation**: Titles from filenames, dates from file modification time
* **Error Recovery**: Graceful handling of malformed content
* **SEO Optimization**: Comprehensive meta tags, Open Graph, Twitter Cards

## Build System & Commands

### Development Commands

```bash
# Run development server with hot reloading
uv run python app/main.py

# Code quality and formatting
uv run ruff format .               # Format all code
uv run ruff check . --fix          # Lint and auto-fix issues

# Run tests
uv run pytest

# Clear application caches (during development)
# Visit http://localhost:8080/admin/cache?token=<your-token> and click "Clear All Caches"
```

### Production Build Commands

```bash
# Build standalone executable
uv run python build.py             # Full build process
uv run python build.py --spec-only # Create spec file only
uv run python build.py --clean     # Clean build artifacts

# Test the executable
cd dist && ./nicegui-blog          # Unix/macOS
cd dist && nicegui-blog.exe        # Windows
```

### Performance Testing

---

## Deployment

This application can be self-hosted using a reverse proxy like Caddy or Nginx. The following instructions are for a macOS environment using Caddy managed by Homebrew.

### Prerequisites

* **Homebrew:** The missing package manager for macOS.
* **Caddy:** A powerful, enterprise-ready, open source web server with automatic HTTPS.

### Setup Instructions

1. **Install Caddy:**

    ```bash
    brew install caddy
    ```

2. **Create a Caddyfile:**

    Create a file named `Caddyfile` in the root of the project directory with the following content:

    ```
    localhost {
        reverse_proxy localhost:8080
    }
    ```

    *Note: If you are using a domain, replace `localhost` with your domain name.*

3. **Start the Application:**

    Run the application using `uv`:

    ```bash
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 &
    ```

4. **Start Caddy:**

    Start the Caddy service:

    ```bash
    brew services start caddy
    ```

    To restart the service after making changes to the `Caddyfile`:

    ```bash
    brew services restart caddy
    ```

Your application will now be available at `http://localhost` (or your domain).

### Performance Testing

```bash
# Test cache performance
curl -w "@curl-format.txt" http://localhost:8080/blog

# Monitor memory usage
ps aux | grep nicegui-blog

```

## Technology & Features

<div align="center">

### **Dark Theme Stack**

<table>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/UI_Framework-NiceGUI_v2.22.1-713A90?style=for-the-badge&logo=fastapi" alt="NiceGUI"><br>
<sub>Modern Python UI with dark theme support</sub>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Styling-Pico.css_+_Custom-713A90?style=for-the-badge&logo=css3" alt="Styling"><br>
<sub>18pt Inter font with purple accents</sub>
</td>
</tr>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/Content-Markdown_+_YAML-713A90?style=for-the-badge&logo=markdown" alt="Content"><br>
<sub>Advanced markdown with syntax highlighting</sub>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Performance-Sub_100ms-713A90?style=for-the-badge&logo=lightning" alt="Performance"><br>
<sub>Multi-layer caching with async processing</sub>
</td>
</tr>
</table>

### **Key Capabilities**

</div>

<table>
<tr>
<td width="33%">

**User Experience**

* Stunning dark theme UI with gradient header
* Purple & orange color scheme
* Lightning-fast performance (sub-100ms cached)
* Real-time search with smart pagination
* Interactive blog statistics
* Precomputed word counts & read times
* Smart content tagging
* Mobile-first responsive design
* Lazy-loaded optimized images
* Smooth scroll animations

</td>
<td width="33%">

**Developer Experience**

* Built-in security validation
* Full TypeScript-style hints
* Modern async/await patterns
* Hot reloading development
* Single executable builds
* Automated code formatting
* Comprehensive error handling

</td>
<td width="33%">

**Architecture**

* Modular component design with @ui.refreshable
* Intelligent multi-layer TTL caching
* XSS prevention & HTML sanitization
* Performance monitoring with metrics
* SEO-friendly URLs & comprehensive meta tags
* Zero database dependencies
* Cross-platform distribution
* Pagination for scalable content
* Image optimization pipeline

</td>
</tr>
</table>

<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/NiceGUI.png" alt="Repository Features Overview" width="300" />
</p>

## License

<div align="center">

<img src="https://img.shields.io/badge/License-MIT-713A90?style=for-the-badge&logo=opensource" alt="MIT License">

**This project is licensed under the MIT License**
*Feel free to use, modify, and distribute*

[View License Details](LICENSE)

</div>

---

<p align="center">
  <a href="https://www.buymeacoffee.com/dunamismax">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" >
  </a>
</p>

<p align="center">
  <a href="https://twitter.com/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Twitter-713A90.svg?&style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://bsky.app/profile/dunamismax.bsky.social" target="_blank"><img src="https://img.shields.io/badge/Bluesky-713A90?style=for-the-badge&logo=bluesky&logoColor=white" alt="Bluesky"></a>
  <a href="https://reddit.com/user/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Reddit-713A90.svg?&style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit"></a>
  <a href="https://discord.com/users/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Discord-713A90.svg?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://signal.me/#p/+dunamismax.66" target="_blank"><img src="https://img.shields.io/badge/Signal-713A90.svg?style=for-the-badge&logo=signal&logoColor=white" alt="Signal"></a>
</p>

---

<p align="center">
  <strong style="color: #713A90; font-size: 18px;">NiceGUI Blog</strong><br>
  <sub style="color: #713A90;">Python 3.13 • Dark Theme • Beautiful UI • Lightning Fast • Zero Database Dependencies • Production Ready</sub>
</p>
