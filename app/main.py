"""Main NiceGUI application for the blog."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from nicegui import app, ui
from pygments.formatters import HtmlFormatter

from content import get_all_posts, get_post_by_slug

if TYPE_CHECKING:
    pass


def generate_syntax_highlighting_css() -> None:
    """Generate CSS file for Pygments syntax highlighting."""
    formatter = HtmlFormatter(
        style="github-dark", cssclass="highlight", noclasses=False
    )
    css_content = formatter.get_style_defs()

    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)

    css_file = static_dir / "syntax.css"
    try:
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css_content)
        print(f"Generated syntax highlighting CSS: {css_file}")
    except OSError as e:
        print(f"Failed to generate syntax CSS: {e}")


def add_global_styles() -> None:
    """Add global styles and fonts to the application using modern NiceGUI patterns."""
    ui.add_head_html(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/static/syntax.css">
    """,
        shared=True,
    )

    # Use ui.add_css for better performance and organization
    ui.add_css("""
        :root {
            --pico-font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            --pico-font-size: 18px;
            --pico-line-height: 1.33;
        }

        body {
            font-family: var(--pico-font-family);
            font-size: var(--pico-font-size);
            line-height: var(--pico-line-height);
        }

        .blog-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .blog-post-card {
            margin-bottom: 1.5rem;
            transition: box-shadow 0.2s ease;
        }

        .blog-post-card:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .blog-post-meta {
            opacity: 0.7;
            font-size: 0.9em;
            margin-bottom: 0.5rem;
        }

        .blog-post-title {
            margin-bottom: 0.5rem;
        }

        .blog-post-summary {
            margin-bottom: 1rem;
        }

        .blog-content {
            max-width: none;
            line-height: 1.7;
        }

        .blog-content h1, .blog-content h2, .blog-content h3,
        .blog-content h4, .blog-content h5, .blog-content h6 {
            margin-top: 2rem;
            margin-bottom: 1rem;
            line-height: 1.3;
        }

        .blog-content p {
            margin-bottom: 1rem;
        }

        .blog-content pre {
            border-radius: 0.5rem;
            overflow-x: auto;
        }

        .highlight {
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }

        .prose {
            color: var(--pico-color);
        }

        .prose img {
            border-radius: 0.5rem;
            max-width: 100%;
            height: auto;
        }
    """)


def create_header() -> ui.element:
    """Create a reusable header component using modern NiceGUI patterns."""
    with (
        ui.row().classes("w-full justify-center") as header_container,
        ui.column().classes("max-w-4xl w-full px-4"),
        ui.element("header").classes("blog-header"),
    ):
        ui.link("My Blog", "/blog", new_tab=False).classes(
            "no-underline text-inherit text-3xl font-bold hover:text-blue-600 transition-colors"
        )
        ui.label("A simple, file-based blog built with NiceGUI").classes(
            "mt-2 opacity-80 text-lg"
        )
    return header_container


def create_footer() -> ui.element:
    """Create a reusable footer component using modern NiceGUI patterns."""
    with (
        ui.row().classes("w-full justify-center mt-auto") as footer_container,
        ui.column().classes("max-w-4xl w-full px-4"),
        ui.element("footer").classes("text-center mt-12 pt-8 border-t border-gray-300"),
        ui.row().classes("justify-center items-center gap-1"),
    ):
        ui.label("© 2025 My Blog. Built with")
        ui.link("NiceGUI", "https://nicegui.io", new_tab=True).classes(
            "text-blue-600 hover:text-blue-800 font-medium"
        )
        ui.label("and ❤️")
    return footer_container


@ui.page("/")
def index() -> None:
    """Root route that redirects to the blog."""
    ui.navigate.to("/blog")


@ui.page("/blog")
def blog_index() -> None:
    """Blog index page displaying all posts using modern NiceGUI patterns."""
    add_global_styles()

    with ui.column().classes("w-full items-center min-h-screen"):
        create_header()

        with (
            ui.row().classes("w-full justify-center flex-grow"),
            ui.column().classes("max-w-4xl w-full px-4"),
        ):
            posts = get_all_posts()

            if not posts:
                with ui.column().classes("items-center gap-6 text-center p-8"):
                    ui.icon("article", size="4rem").classes("text-gray-400")
                    ui.label("No posts yet").classes("text-2xl font-semibold")
                    ui.markdown(
                        "Add some Markdown files to the `content/posts` directory to get started!"
                    ).classes("opacity-80 max-w-md text-center")
            else:
                with ui.column().classes("gap-6"):
                    for post in posts:
                        with ui.card().classes("blog-post-card w-full"):
                            if post.get("date"):
                                ui.label(post["date"].strftime("%B %d, %Y")).classes(
                                    "blog-post-meta text-sm opacity-70 mb-2"
                                )

                            ui.link(
                                post.get("title", "Untitled"),
                                f"/blog/{post['slug']}",
                                new_tab=False,
                            ).classes(
                                "text-xl font-semibold mb-2 no-underline text-inherit hover:text-blue-600 transition-colors block"
                            )

                            if post.get("summary"):
                                ui.label(post["summary"]).classes(
                                    "mb-4 opacity-90 leading-relaxed"
                                )

                            ui.link(
                                "Read more →",
                                f"/blog/{post['slug']}",
                                new_tab=False,
                            ).classes("text-blue-600 hover:text-blue-800 font-medium")

        create_footer()


@ui.page("/blog/{slug}")
def blog_post(slug: str) -> None:
    """Blog post detail page using modern NiceGUI patterns."""
    add_global_styles()

    post = get_post_by_slug(slug)

    if not post:
        with ui.column().classes("w-full items-center min-h-screen"):
            create_header()

            with (
                ui.row().classes("w-full justify-center flex-grow"),
                ui.column().classes("max-w-4xl w-full px-4"),
                ui.column().classes("items-center gap-6 text-center p-8"),
            ):
                ui.icon("error_outline", size="4rem").classes("text-red-400")
                ui.label("Post Not Found").classes("text-2xl font-semibold")
                ui.label("The requested blog post could not be found.").classes(
                    "opacity-80 mb-4"
                )
                ui.button(
                    "← Back to Blog", on_click=lambda: ui.navigate.to("/blog")
                ).props("flat color=primary icon=arrow_back")

            create_footer()
        return

    with ui.column().classes("w-full items-center min-h-screen"):
        create_header()

        with (
            ui.row().classes("w-full justify-center flex-grow"),
            ui.column().classes("max-w-4xl w-full px-4"),
        ):
            # Navigation back button
            ui.button("← Back to Blog", on_click=lambda: ui.navigate.to("/blog")).props(
                "flat color=primary icon=arrow_back"
            ).classes("mb-6 self-start")

            # Article header
            with ui.column().classes("mb-8"):
                ui.label(post.get("title", "Untitled")).classes(
                    "text-4xl font-bold mb-4 leading-tight"
                )

                if post.get("date"):
                    ui.label(post["date"].strftime("%B %d, %Y")).classes(
                        "text-sm opacity-70 mb-6"
                    )

            # Article content with improved styling
            ui.html(post["content"]).classes("blog-content prose prose-lg max-w-none")

        create_footer()


app.add_static_files("/static", "static")


@app.on_startup
def startup() -> None:
    """Generate syntax highlighting CSS on startup."""
    generate_syntax_highlighting_css()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="My Blog",
        port=8080,
        show_welcome_message=False,
        reload=True,
        favicon="🏠",
    )
