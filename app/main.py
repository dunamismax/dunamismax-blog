"""Main NiceGUI application for the blog."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from cachetools import TTLCache
from nicegui import app, ui
from pygments.formatters import HtmlFormatter

from app.content import get_all_posts, get_post_by_slug

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Memory-based cache for posts (TTL: 10 minutes)
posts_cache: TTLCache[str, list[dict[str, Any]]] = TTLCache(maxsize=100, ttl=600)
content_cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=50, ttl=1200)


def get_cached_posts() -> list[dict[str, Any]]:
    """Get all posts with caching for improved performance."""
    cache_key = "all_posts"
    try:
        return posts_cache[cache_key]
    except KeyError:
        posts = get_all_posts()
        posts_cache[cache_key] = posts
        logger.info(f"Cached {len(posts)} posts")
        return posts


def get_cached_post(slug: str) -> dict[str, Any] | None:
    """Get a single post with caching for improved performance."""
    if slug in content_cache:
        logger.info(f"Serving post '{slug}' from cache")
        return content_cache[slug]

    post = get_post_by_slug(slug)
    if post:
        content_cache[slug] = post
        logger.info(f"Cached post '{slug}'")
    return post


def clear_cache() -> None:
    """Clear all caches - useful for development or content updates."""
    posts_cache.clear()
    content_cache.clear()
    logger.info("All caches cleared")


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
        logger.info("Generated syntax highlighting CSS: %s", css_file)
    except OSError as e:
        logger.error("Failed to generate syntax CSS: %s", e)


def add_global_styles() -> None:
    """Add global styles and fonts to the application using modern NiceGUI patterns."""
    # Set page theme to dark
    ui.dark_mode().enable()

    ui.add_head_html(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/static/syntax.css">
        <meta name="theme-color" content="#1E1E2E">
        <meta name="description" content="A modern, fast blog built with NiceGUI and Python">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta property="og:type" content="website">
        <meta property="og:title" content="My Modern NiceGUI Blog">
        <meta property="og:description" content="A lightning-fast blog built with NiceGUI v2.22.1">
    """,
        shared=True,
    )

    # Use ui.add_css for better performance and organization
    ui.add_css("""
        :root {
            --pico-font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            --pico-font-size: 18px;
            --pico-line-height: 1.33;

            /* Dark theme color scheme */
            --dark-bg: #1E1E2E;
            --purple-accent: #713A90;
            --orange-accent: #D77757;
            --text-primary: #FFFFFF;
            --text-secondary: #B4B4B4;
            --card-bg: #2A2A3E;
            --border-color: #3A3A4E;
        }

        /* Force dark theme */
        [data-theme="dark"],
        :root:not([data-theme="light"]) {
            --pico-background-color: var(--dark-bg);
            --pico-color: var(--text-primary);
            --pico-card-background-color: var(--card-bg);
            --pico-border-color: var(--border-color);
            --pico-primary: var(--purple-accent);
            --pico-secondary: var(--orange-accent);
        }

        body {
            font-family: var(--pico-font-family);
            font-size: var(--pico-font-size);
            line-height: var(--pico-line-height);
            background-color: var(--dark-bg);
            color: var(--text-primary);
        }

        .blog-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .blog-header a {
            color: var(--purple-accent);
        }

        .blog-header a:hover {
            color: var(--orange-accent);
        }

        .blog-post-card {
            margin-bottom: 1.5rem;
            transition: box-shadow 0.2s ease;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
        }

        .blog-post-card:hover {
            box-shadow: 0 8px 25px rgba(113, 58, 144, 0.2);
            border-color: var(--purple-accent);
        }

        .blog-post-meta {
            color: var(--text-secondary);
            font-size: 16px;
            margin-bottom: 0.5rem;
        }

        .blog-post-title {
            margin-bottom: 0.5rem;
        }

        .blog-post-card a {
            color: var(--text-primary);
        }

        .blog-post-card a:hover {
            color: var(--purple-accent);
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
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color);
        }

        .prose {
            color: var(--text-primary);
        }

        .prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
            color: var(--purple-accent);
        }

        .prose a {
            color: var(--orange-accent);
        }

        .prose a:hover {
            color: var(--purple-accent);
        }

        .prose img {
            border-radius: 0.5rem;
            max-width: 100%;
            height: auto;
        }

        .scroll-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 1000;
            transition: opacity 0.3s ease;
        }

        .search-container {
            position: relative;
            margin-bottom: 2rem;
        }

        .blog-stats {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 2rem;
            text-align: center;
        }

        .loading-skeleton {
            background: linear-gradient(90deg, var(--card-bg) 25%, var(--border-color) 50%, var(--card-bg) 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }

        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Input and form styling */
        input, textarea, select {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            font-family: var(--pico-font-family) !important;
            font-size: var(--pico-font-size) !important;
        }

        input:focus, textarea:focus, select:focus {
            border-color: var(--purple-accent) !important;
            box-shadow: 0 0 0 1px var(--purple-accent) !important;
        }

        /* Button styling */
        button {
            background-color: var(--purple-accent) !important;
            color: white !important;
            border: none !important;
        }

        button:hover {
            background-color: var(--orange-accent) !important;
        }

        /* Footer styling */
        footer {
            border-top: 1px solid var(--border-color) !important;
            color: var(--text-secondary);
        }

        @media (max-width: 768px) {
            .blog-header {
                margin-bottom: 1rem;
            }

            .scroll-to-top {
                bottom: 1rem;
                right: 1rem;
            }
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
            "no-underline text-3xl font-bold transition-colors"
        ).style("color: var(--purple-accent)")
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
            "font-medium"
        ).style("color: var(--purple-accent)")
        ui.label("and love")
    return footer_container


@ui.refreshable
def create_search_bar() -> ui.element:
    """Create a modern search bar component with reactive filtering."""
    with ui.row().classes("search-container w-full max-w-md") as search_container:
        search_input = (
            ui.input(
                placeholder="Search posts...", on_change=lambda e: filter_posts(e.value)
            )
            .props("outlined dense")
            .classes("flex-grow")
        )
        search_input.props("prepend-icon=search")
    return search_container


def filter_posts(query: str) -> None:
    """Filter posts based on search query."""
    if not query:
        return
    # Enhanced search implementation
    posts = get_cached_posts()
    filtered = [
        post
        for post in posts
        if query.lower() in post.get("title", "").lower()
        or query.lower() in post.get("summary", "").lower()
        or any(query.lower() in tag.lower() for tag in post.get("tags", []))
    ]
    logger.info(f"Found {len(filtered)} posts matching '{query}'")
    # Note: Full reactive implementation would require UI state management


def create_blog_stats(posts: list) -> ui.element:
    """Create a stats card showing blog metrics."""
    with (
        ui.card().classes("blog-stats w-full max-w-md") as stats_card,
        ui.row().classes("justify-around items-center"),
    ):
        with ui.column().classes("items-center"):
            ui.label(str(len(posts))).classes("text-2xl font-bold").style(
                "color: var(--purple-accent)"
            )
            ui.label("Posts").classes("text-sm opacity-70")

        with ui.column().classes("items-center"):
            total_words = sum(post.get("word_count", 0) for post in posts)
            ui.label(f"{total_words:,}").classes("text-2xl font-bold").style(
                "color: var(--orange-accent)"
            )
            ui.label("Words").classes("text-sm opacity-70")

        with ui.column().classes("items-center"):
            avg_read_time = max(1, total_words // len(posts) // 200) if posts else 0
            ui.label(f"{avg_read_time}").classes("text-2xl font-bold").style(
                "color: var(--purple-accent)"
            )
            ui.label("Min Read").classes("text-sm opacity-70")
    return stats_card


def create_scroll_to_top() -> ui.element:
    """Create a floating scroll-to-top button."""
    with (
        ui.button(
            icon="keyboard_arrow_up",
            on_click="window.scrollTo({top: 0, behavior: 'smooth'})",
        )
        .props("fab")
        .classes("scroll-to-top") as scroll_btn
    ):
        pass
    return scroll_btn


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
            posts = get_cached_posts()

            # Add search bar and stats
            with ui.row().classes("w-full justify-center mb-6"):
                create_search_bar()

            if posts:
                create_blog_stats(posts)

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
                            # Post metadata row
                            with ui.row().classes("justify-between items-center mb-2"):
                                if post.get("date"):
                                    ui.label(
                                        post["date"].strftime("%B %d, %Y")
                                    ).classes("blog-post-meta text-sm opacity-70")

                                # Reading time estimation
                                word_count = post.get("word_count", 0)
                                read_time = post.get(
                                    "read_time", max(1, word_count // 200)
                                )
                                ui.label(f"{read_time} min read").classes(
                                    "text-sm opacity-60"
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

                            # Enhanced action row with tags if available
                            with ui.row().classes("justify-between items-center"):
                                ui.link(
                                    "Read more →",
                                    f"/blog/{post['slug']}",
                                    new_tab=False,
                                ).classes("font-medium").style(
                                    "color: var(--orange-accent)"
                                )

                                # Add tags if they exist
                                if post.get("tags"):
                                    with ui.row().classes("gap-1"):
                                        for tag in post["tags"][:3]:  # Show max 3 tags
                                            ui.label(f"#{tag}").classes(
                                                "text-xs px-2 py-1 rounded-full"
                                            ).style(
                                                "background-color: var(--purple-accent); color: white"
                                            )

        # Add scroll to top button
        create_scroll_to_top()
        create_footer()


@ui.page("/blog/{slug}")
def blog_post(slug: str) -> None:
    """Blog post detail page using modern NiceGUI patterns."""
    add_global_styles()

    post = get_cached_post(slug)

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
                ).props("flat icon=arrow_back").style("color: var(--purple-accent)")

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
                "flat icon=arrow_back"
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

            # Article footer with tags and sharing
            with ui.row().classes(
                "justify-between items-center mt-8 pt-6 border-t border-gray-300"
            ):
                # Tags section
                if post.get("tags"):
                    with ui.column().classes("gap-2"):
                        ui.label("Tags:").classes("text-sm font-medium opacity-70")
                        with ui.row().classes("gap-2 flex-wrap"):
                            for tag in post["tags"]:
                                ui.label(f"#{tag}").classes(
                                    "text-sm px-3 py-1 rounded-full cursor-pointer transition-colors"
                                ).style(
                                    "background-color: var(--purple-accent); color: white"
                                )

                # Social sharing (placeholder)
                with ui.row().classes("gap-2"):
                    ui.button("Share", icon="share").props("flat size=sm").style(
                        "color: var(--orange-accent)"
                    )
                    ui.button("", icon="bookmark_border").props("flat size=sm")

            # Navigation to other posts
            all_posts = get_cached_posts()
            current_index = next(
                (i for i, p in enumerate(all_posts) if p["slug"] == slug), -1
            )

            if current_index >= 0:
                with ui.row().classes("justify-between mt-8 gap-4"):
                    # Previous post
                    if current_index < len(all_posts) - 1:
                        prev_post = all_posts[current_index + 1]
                        with ui.card().classes(
                            "flex-1 cursor-pointer hover:shadow-lg transition-shadow"
                        ):
                            ui.link(
                                f"← {prev_post.get('title', 'Previous Post')}",
                                f"/blog/{prev_post['slug']}",
                                new_tab=False,
                            ).classes(
                                "text-sm font-medium no-underline text-inherit hover:text-blue-600"
                            )
                    else:
                        ui.element("div").classes("flex-1")  # Spacer

                    # Next post
                    if current_index > 0:
                        next_post = all_posts[current_index - 1]
                        with ui.card().classes(
                            "flex-1 cursor-pointer hover:shadow-lg transition-shadow text-right"
                        ):
                            ui.link(
                                f"{next_post.get('title', 'Next Post')} →",
                                f"/blog/{next_post['slug']}",
                                new_tab=False,
                            ).classes(
                                "text-sm font-medium no-underline text-inherit hover:text-blue-600"
                            )

        # Add scroll to top button
        create_scroll_to_top()
        create_footer()


@ui.page("/admin/cache")
def admin_cache() -> None:
    """Admin route for cache management - basic security through obscurity."""
    add_global_styles()

    with (
        ui.column().classes("w-full items-center min-h-screen"),
        ui.card().classes("max-w-md w-full mt-8"),
    ):
        ui.label("Cache Management").classes("text-xl font-bold mb-4")

        with ui.row().classes("gap-4 w-full"):
            ui.button(
                "Clear All Caches",
                on_click=lambda: (
                    clear_cache(),
                    ui.notify("Caches cleared!", type="positive"),
                ),
            ).props("").style("background-color: var(--purple-accent); color: white")

            ui.button("View Stats", on_click=lambda: show_cache_stats()).props(
                "color=secondary"
            )

        # Cache statistics
        with ui.column().classes("w-full mt-4") as stats_container:
            stats_container.clear()
            with stats_container:
                ui.label(f"Posts Cache: {len(posts_cache)} items").classes("text-sm")
                ui.label(f"Content Cache: {len(content_cache)} items").classes(
                    "text-sm"
                )


def show_cache_stats() -> None:
    """Display cache statistics."""
    ui.notify(f"Posts: {len(posts_cache)}, Content: {len(content_cache)}", type="info")


app.add_static_files("/static", "../static")


@app.on_startup
def startup() -> None:
    """Generate syntax highlighting CSS on startup."""
    generate_syntax_highlighting_css()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="My Modern NiceGUI Blog",
        port=8080,
        show_welcome_message=False,
        reload=True,
        favicon="https://nicegui.io/favicon.ico",
        dark=True,
    )
