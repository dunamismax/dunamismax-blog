"""Main NiceGUI application for the blog."""

from __future__ import annotations

import hmac
import logging
import os
from pathlib import Path
from typing import Any

from cachetools import TTLCache
from fastapi import Request
from nicegui import app, ui
from pygments.formatters import HtmlFormatter

from app.content import get_all_posts, get_post_by_slug

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Memory-based cache for posts (TTL: 10 minutes)
posts_cache: TTLCache[str, list[dict[str, Any]]] = TTLCache(maxsize=100, ttl=600)
content_cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=50, ttl=1200)

# Current list of posts shown on the index page
filtered_posts: list[dict[str, Any]] = []


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


def is_admin_authorized(request: Request) -> bool:
    """Return True if the request provides the correct admin token."""
    token = os.getenv("BLOG_ADMIN_TOKEN")
    if not token:
        logger.warning("Admin token not configured")
        return False
    provided = request.query_params.get("token", "")
    return hmac.compare_digest(provided, token)


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
    """Add global styles and external stylesheets."""
    ui.dark_mode().enable()
    ui.add_head_html(
        """
        <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css\">
        <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
        <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
        <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">
        <link rel=\"stylesheet\" href=\"/static/syntax.css\">
        <link rel=\"stylesheet\" href=\"/static/blog.css\">
        <meta name=\"theme-color\" content=\"#1E1E2E\">
        <meta name=\"description\" content=\"A modern, fast blog built with NiceGUI and Python\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <meta property=\"og:type\" content=\"website\">
        <meta property=\"og:title\" content=\"My Modern NiceGUI Blog\">
        <meta property=\"og:description\" content=\"A lightning-fast blog built with NiceGUI v2.22.1\">
    """,
        shared=True,
    )


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
    """Filter posts based on search query and refresh UI."""
    global filtered_posts
    posts = get_cached_posts()
    filtered_posts = apply_filter(query, posts)
    logger.info(f"Found {len(filtered_posts)} posts matching '{query}'")
    render_posts.refresh()


def apply_filter(query: str, posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return posts that match a query in title, summary, or tags."""
    if not query:
        return posts
    q = query.lower()
    return [
        post
        for post in posts
        if q in post.get("title", "").lower()
        or q in post.get("summary", "").lower()
        or any(q in tag.lower() for tag in post.get("tags", []))
    ]


def create_blog_stats(posts: list[dict[str, Any]]) -> ui.element:
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


@ui.refreshable
def render_posts() -> None:
    """Render the list of posts based on the current filter."""
    if not filtered_posts:
        with ui.column().classes("items-center gap-6 text-center p-8"):
            ui.icon("article", size="4rem").classes("text-gray-400")
            ui.label("No posts yet").classes("text-2xl font-semibold")
            ui.markdown(
                "Add some Markdown files to the `content/posts` directory to get started!"
            ).classes("opacity-80 max-w-md text-center")
        return

    with ui.column().classes("gap-6"):
        for post in filtered_posts:
            with ui.card().classes("blog-post-card w-full"):
                with ui.row().classes("justify-between items-center mb-2"):
                    if post.get("date"):
                        ui.label(post["date"].strftime("%B %d, %Y")).classes(
                            "blog-post-meta text-sm opacity-70"
                        )

                    word_count = post.get("word_count", 0)
                    read_time = post.get("read_time", max(1, word_count // 200))
                    ui.label(f"{read_time} min read").classes("text-sm opacity-60")

                ui.link(
                    post.get("title", "Untitled"),
                    f"/blog/{post['slug']}",
                    new_tab=False,
                ).classes(
                    "text-xl font-semibold mb-2 no-underline text-inherit hover:text-blue-600 transition-colors block"
                )

                if post.get("summary"):
                    ui.label(post["summary"]).classes("mb-4 opacity-90 leading-relaxed")

                with ui.row().classes("justify-between items-center"):
                    ui.link(
                        "Read more →",
                        f"/blog/{post['slug']}",
                        new_tab=False,
                    ).classes("font-medium").style("color: var(--orange-accent)")

                    if post.get("tags"):
                        with ui.row().classes("gap-1"):
                            for tag in post["tags"][:3]:
                                ui.label(f"#{tag}").classes(
                                    "text-xs px-2 py-1 rounded-full"
                                ).style(
                                    "background-color: var(--purple-accent); color: white"
                                )


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
    """Blog index page displaying all posts."""
    add_global_styles()

    with ui.column().classes("w-full items-center min-h-screen"):
        create_header()

        with (
            ui.row().classes("w-full justify-center flex-grow"),
            ui.column().classes("max-w-4xl w-full px-4"),
        ):
            posts = get_cached_posts()
            filtered_posts[:] = posts

            with ui.row().classes("w-full justify-center mb-6"):
                create_search_bar()

            if filtered_posts:
                create_blog_stats(filtered_posts)

            render_posts()

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
def admin_cache(request: Request) -> None:
    """Admin route for cache management protected by a token."""
    add_global_styles()

    if not is_admin_authorized(request):
        with ui.column().classes("w-full items-center min-h-screen"):
            ui.label("Unauthorized").classes("text-red-500 text-xl mt-8")
        return

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


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.add_static_files("/static", str(STATIC_DIR))


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
