<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/NiceBlog.png" alt="NiceGUI Dark Blog" width="400" />
</p>

<p align="center">
  <a href="https://github.com/dunamismax/nicegui-blog">
    <img src="https://readme-typing-svg.demolab.com/?font=Inter&weight=600&size=26&pause=800&color=713A90&center=true&vCenter=true&width=1200&height=80&lines=Dark+Theme+NiceGUI+Blog+Application;Python+3.13+%2B+NiceGUI+2.22.1;Purple+%26+Orange+Aesthetic+Design;Lightning+Fast+TTL+Cached+Content;Precomputed+Word+Count+%26+Read+Time;Real+Time+Search+%26+Statistics;File+Based+Content+Management;Zero+Database+Dependencies;Standalone+Executable+Distribution;MIT+Licensed+Open+Source" alt="Typing SVG" />
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

# NiceGUI Dark Blog

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
<sub><b>Zero Dependencies</b></sub>
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-Standalone-713A90?style=for-the-badge&logo=package&logoColor=white" alt="Standalone"><br>
<sub><b>Single Executable</b></sub>
</td>
</tr>
</table>

<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/Repo-Features.png" alt="Repository Features" width="400" />
</p>

## Project Structure

```sh
nicegui-blog/
├── app/                      # Application source
│   ├── main.py              # NiceGUI application with modern UI patterns
│   └── content.py           # Robust content loading with error handling
├── content/                 # Blog content
│   └── posts/               # Markdown blog posts with front matter
├── static/                  # Static assets
│   └── syntax.css           # Auto-generated Pygments styling
├── tests/                   # Test suite
├── build.py                 # PyInstaller build script
└── pyproject.toml           # Modern Python project configuration
```

---

## Quick Start

**Prerequisites:** Python 3.13+ and uv package manager

```bash
# Install uv package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the repository
git clone <repository-url>
cd nicegui-blog

# Setup Python 3.13 environment and dependencies
uv python install 3.13
uv python pin 3.13
uv sync

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
<td>Main blog index with dark theme, search, and statistics</td>
<td><img src="https://img.shields.io/badge/-Main-713A90?style=flat" alt="Main"></td>
</tr>
<tr>
<td><code>/blog/&lt;slug&gt;</code></td>
<td>Individual blog posts with beautiful typography</td>
<td><img src="https://img.shields.io/badge/-Posts-713A90?style=flat" alt="Posts"></td>
</tr>
<tr>
<td><code>/admin/cache</code></td>
<td>Cache management interface</td>
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

### Supported Features

- **Multi-Format Dates**: ISO, YYYY-MM-DD, natural language formats
- **Advanced Markdown**: Tables, task lists, syntax highlighting, TOC generation
- **Auto-Generation**: Titles from filenames, dates from file modification time
- **Error Recovery**: Graceful handling of malformed content

## Build System & Commands

### Development Commands

```bash
# Run development server with hot reloading
uv run python app/main.py

# Code quality and formatting
uv run ruff format .               # Format all code
uv run ruff check . --fix          # Lint and auto-fix issues

# Clear application caches (during development)
# Visit http://localhost:8080/admin/cache and click "Clear All Caches"
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

- Stunning dark theme UI
- Purple color scheme
- Lightning-fast performance
- Real-time search functionality
- Interactive blog statistics
- Precomputed word counts & read times
- Smart content tagging
- Mobile-first responsive design

</td>
<td width="33%">

**Developer Experience**

- Built-in security validation
- Full TypeScript-style hints
- Modern async/await patterns
- Hot reloading development
- Single executable builds
- Automated code formatting
- Comprehensive error handling

</td>
<td width="33%">

**Architecture**

- Modular component design
- Intelligent caching system
- XSS prevention & validation
- Performance monitoring
- SEO-friendly URLs
- Zero database dependencies
- Cross-platform distribution

</td>
</tr>
</table>

<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/NiceGUI.png" alt="Repository Features Overview" width="400" />
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
  <strong style="color: #713A90; font-size: 18px;">NiceGUI Dark Blog</strong><br>
  <sub style="color: #713A90;">Python 3.13 • Dark Theme • Beautiful UI • Lightning Fast • Zero Dependencies • Production Ready</sub>
</p>
