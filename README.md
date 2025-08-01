<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/NiceGUI-Blog-Image.png" alt="NiceGUI Blog Application" width="350" />
</p>

<p align="center">
  <a href="https://github.com/dunamismax/nicegui-blog">
    <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=24&pause=1000&color=2B5CE6&center=true&vCenter=true&width=1000&lines=Modern+Python+3.13+Blog+Application;NiceGUI+v2.22.1+Latest+Features+Integration;File+Based+Content+Management+System;Zero+Database+Dependencies+Architecture;Standalone+Executable+with+PyInstaller;Syntax+Highlighting+with+Pygments+Support;Responsive+Design+with+Modern+CSS;Real+Time+Markdown+Processing;Professional+Typography+with+Inter+Font;Production+Ready+Error+Handling;Multi+Format+Date+Support+Built+In;Interactive+UI+Components+and+Transitions;Enhanced+Developer+Experience+with+uv;Ruff+Formatting+and+Linting+Integration;Cross+Platform+Desktop+Distribution;Mobile+Friendly+Responsive+Layout;GitHub+Dark+Theme+Syntax+Highlighting;Advanced+Markdown+Extensions+Support;Type+Safe+Python+Programming;Lightning+Fast+Static+File+Serving;MIT+Licensed+Open+Source+Excellence" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3130/"><img src="https://img.shields.io/badge/Python-3.13+-2B5CE6.svg?logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://nicegui.io/"><img src="https://img.shields.io/badge/NiceGUI-v2.22.1-00D4AA.svg?logo=fastapi&logoColor=white" alt="NiceGUI Version"></a>
  <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/uv-Package_Manager-FF6B35.svg" alt="uv Package Manager"></a>
  <a href="https://pyinstaller.org/"><img src="https://img.shields.io/badge/PyInstaller-v6.14.2-4B8BBE.svg" alt="PyInstaller"></a>
  <a href="https://docs.astral.sh/ruff/"><img src="https://img.shields.io/badge/Ruff-Formatted-D7FF64.svg" alt="Ruff Formatting"></a>
  <a href="https://pygments.org/"><img src="https://img.shields.io/badge/Pygments-Syntax_Highlighting-FFD43B.svg" alt="Pygments"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
</p>

---

# NiceGUI Blog

Modern file-based blog application built with Python 3.13 and NiceGUI v2.22.1, featuring standalone executable packaging and production-ready architecture.

## Core Features

- **Python 3.13**: Latest Python with enhanced performance and modern syntax
- **NiceGUI v2.22.1**: Modern UI components with responsive design
- **File-Based CMS**: Zero database dependencies, markdown-powered content
- **Standalone Executables**: PyInstaller integration for easy distribution

<p align="center">
  <img src="https://github.com/dunamismax/images/blob/main/python/python-checklist.png" alt="Python Development Checklist" width="400" />
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
├── build.py                 # PyInstaller build script
├── nicegui-blog.spec        # PyInstaller configuration
└── pyproject.toml           # Modern Python project configuration
```

---

## Quick Start

**Prerequisites:** Python 3.13+ and uv package manager

```bash
# Install uv and setup environment
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone <repository-url>
cd nicegui-blog

# Setup Python 3.13 environment
uv python install 3.13
uv python pin 3.13
uv sync

# Run the application
uv run python app/main.py
```

Application available at `http://localhost:8080`

---

## Content Management

### Creating Blog Posts

```markdown
---
title: "Your Post Title"
date: "2025-01-15"
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

## Build System

```bash
# Development
uv run python app/main.py          # Run development server
uv run ruff format .               # Format code
uv run ruff check . --fix          # Lint and fix issues

# Production
uv run python build.py             # Build standalone executable
uv run python build.py --clean     # Clean build artifacts

# Distribution
cd dist && ./nicegui-blog          # Run standalone executable
```

## Technology Stack

- **UI Framework**: NiceGUI v2.22.1 with modern component patterns
- **Styling**: Pico.css + custom CSS with Inter font typography
- **Content**: Python-markdown with Pygments syntax highlighting
- **Package Management**: uv for fast dependency resolution
- **Code Quality**: Ruff for formatting and linting
- **Distribution**: PyInstaller for cross-platform executables

## Key Improvements

- **Enhanced UI**: Modern NiceGUI patterns with hover effects and transitions
- **Robust Error Handling**: Comprehensive content validation and recovery
- **Type Safety**: Full type hints using Python 3.13 syntax
- **Production Ready**: Memory-safe operations with comprehensive testing
- **Developer Experience**: Modern tooling with uv and ruff integration
- **Cross-Platform**: Standalone executables for Windows, macOS, and Linux

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <a href="https://www.buymeacoffee.com/dunamismax">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" >
  </a>
</p>

<p align="center">
  <a href="https://twitter.com/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://bsky.app/profile/dunamismax.bsky.social" target="_blank"><img src="https://img.shields.io/badge/Bluesky-blue?style=for-the-badge&logo=bluesky&logoColor=white" alt="Bluesky"></a>
  <a href="https://reddit.com/user/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Reddit-%23FF4500.svg?&style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit"></a>
  <a href="https://discord.com/users/dunamismax" target="_blank"><img src="https://img.shields.io/badge/Discord-dunamismax-7289DA.svg?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://signal.me/#p/+dunamismax.66" target="_blank"><img src="https://img.shields.io/badge/Signal-dunamismax.66-3A76F0.svg?style=for-the-badge&logo=signal&logoColor=white" alt="Signal"></a>
</p>

---

<p align="center">
  <strong>NiceGUI Blog</strong><br>
  <sub>Python 3.13 • NiceGUI v2.22.1 • File-Based CMS • Standalone Executables • Modern UI • Type Safe • Zero Dependencies</sub>
</p>
