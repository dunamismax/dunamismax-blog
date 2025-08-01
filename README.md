# NiceGUI Blog

A modern, file-based blog application built with **NiceGUI v2.22.1** and **Python 3.13**. This enhanced version features improved UI components, robust error handling, and standalone executable packaging.

## ✨ New Features & Improvements

### **Latest Technology Stack**

- **Python 3.13** - Latest Python version with enhanced performance
- **NiceGUI v2.22.1** - Latest version with modern UI patterns and components
- **Enhanced Error Handling** - Robust content loading with multiple date format support
- **Modern UI Components** - Updated with latest NiceGUI patterns and better UX
- **PyInstaller Integration** - Create standalone executables for easy distribution

### **UI/UX Enhancements**

- **Modern Design**: Clean, professional interface with improved typography
- **Responsive Layout**: Better mobile and desktop experience
- **Interactive Elements**: Hover effects, transitions, and improved navigation
- **Enhanced Typography**: Better readability with Inter font family
- **Improved Cards**: Hover effects and better spacing for blog post cards
- **Better Error Pages**: User-friendly 404 pages with clear navigation

### **Developer Experience**

- **Ruff Formatting**: Code formatted and linted to modern Python standards
- **Type Safety**: Enhanced type hints throughout the codebase
- **Better Documentation**: Comprehensive docstrings and comments
- **Modular Architecture**: Clean separation of concerns

## Tech Stack

- **Web Framework:** NiceGUI v2.22.1 (latest version)
- **Styling:** Pico.css + Custom CSS with modern patterns
- **Content Processing:** python-markdown with advanced extensions
- **Syntax Highlighting:** Pygments with GitHub Dark theme
- **Package Management:** uv (fast Python package manager)
- **Code Quality:** ruff (modern Python linter and formatter)
- **Packaging:** PyInstaller v6.14.2 for standalone executables

## 🚀 Quick Start

### Prerequisites

- **Python 3.13** or later
- **uv** (recommended) or pip for package management

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repository-url>
cd nicegui-blog

# Install Python 3.13 and setup environment
uv python install 3.13
uv python pin 3.13
uv sync

# Run the application
uv run python app/main.py
```

### Option 2: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd nicegui-blog

# Create virtual environment with Python 3.13
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python app/main.py
```

The application will be available at `http://localhost:8080`

## 📝 Content Management

### Adding Blog Posts

1. Create `.md` files in the `content/posts/` directory
2. Include front matter at the top of each file:

```markdown
---
title: "Your Post Title"
date: "2025-01-15"
summary: "A brief description of your post"
---

# Your Post Content

Write your blog post content here using Markdown.

## Code Highlighting

```python
def hello_world():
    print("Hello, NiceGUI!")
```

## Features Supported

- Tables
- Task lists
- Links
- Images
- And much more!

```

### Supported Front Matter Fields

- `title`: Post title (auto-generated from filename if missing)
- `date`: Publication date (supports multiple formats: ISO, YYYY-MM-DD, etc.)
- `summary`: Brief description for the post listing
- `author`: Post author (optional)
- `tags`: List of tags (optional)

### Markdown Extensions

The blog supports advanced Markdown features:
- **Syntax highlighting** with Pygments
- **Tables** and **task lists**
- **Table of contents** generation
- **Magic links** for URLs and social media
- **Custom fences** including Mermaid diagrams
- **Math expressions** and **emoji**

## 🏗️ Development

### Code Quality

The project uses **Ruff** for formatting and linting:

```bash
# Format code
uv run ruff format .

# Check and fix linting issues
uv run ruff check . --fix
```

### Project Structure

```
nicegui-blog/
├── app/
│   ├── main.py          # Main NiceGUI application
│   └── content.py       # Content loading and processing
├── content/
│   └── posts/           # Blog post markdown files
├── static/
│   └── syntax.css       # Auto-generated syntax highlighting
├── build.py             # PyInstaller build script
├── nicegui-blog.spec    # PyInstaller configuration
└── pyproject.toml       # Project configuration
```

## 📦 Building Standalone Executable

Create a standalone executable that can run without Python installed:

### Quick Build

```bash
# Using the build script
uv run python build.py

# Or manually with PyInstaller
uv run pyinstaller nicegui-blog.spec
```

### Build Options

```bash
# Clean previous builds
uv run python build.py --clean

# Create only the spec file
uv run python build.py --spec-only

# Standard build (creates executable in dist/)
uv run python build.py
```

### Running the Executable

After building:

```bash
cd dist
./nicegui-blog  # On Linux/macOS
# or
nicegui-blog.exe  # On Windows
```

The executable includes:

- All Python dependencies
- Content and static files
- Syntax highlighting themes
- Complete blog functionality

## 🔧 Configuration

### Environment Variables

- `UV_PROJECT_ENVIRONMENT`: Custom virtual environment path
- `PYTHONPATH`: Additional Python paths if needed

### Customization

1. **Styling**: Modify CSS in `app/main.py` `add_global_styles()` function
2. **Content**: Update posts in `content/posts/`
3. **Static Files**: Add assets to `static/` directory
4. **Themes**: Modify Pygments theme in `generate_syntax_highlighting_css()`

## 🚀 Deployment

### Local Development

```bash
uv run python app/main.py
```

### Production Deployment

```bash
# Build and distribute executable
uv run python build.py
```

### Docker (Optional)

The application can be containerized using the NiceGUI Docker patterns. See NiceGUI documentation for details.

## 🆕 Upgrade Summary

This version includes comprehensive upgrades:

### **Technology Upgrades**

- ✅ Python 3.13 compatibility
- ✅ NiceGUI v2.22.1 (latest version)
- ✅ PyInstaller v6.14.2 integration
- ✅ Modern dependency management with uv

### **Code Quality Improvements**

- ✅ Ruff formatting and linting
- ✅ Enhanced error handling
- ✅ Better type safety
- ✅ Comprehensive documentation

### **UI/UX Enhancements**

- ✅ Modern NiceGUI patterns
- ✅ Improved responsive design
- ✅ Better typography and spacing
- ✅ Enhanced user interactions

### **Developer Experience**

- ✅ Simplified build process
- ✅ Better project structure
- ✅ Comprehensive build instructions
- ✅ Multiple deployment options

## 📋 Build Commands Summary

```bash
# Setup environment from scratch
uv python install 3.13 && uv sync

# Run in development mode
uv run python app/main.py

# Build standalone executable
uv run python build.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Format with `uv run ruff format .`
5. Check with `uv run ruff check . --fix`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using NiceGUI v2.22.1 and Python 3.13**
