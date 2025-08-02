"""Main NiceGUI application for the blog."""

from __future__ import annotations

import asyncio
import hmac
import json
import logging
import os
from pathlib import Path
from typing import Any

import redis.asyncio as redis
from cachetools import TTLCache
from fastapi import Request
from nicegui import app, ui
from pygments.formatters import HtmlFormatter

from app.content import get_all_posts, get_post_by_slug

POSTS_CACHE_TTL = 600
CONTENT_CACHE_TTL = 1200

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posts_cache: TTLCache[str, list[dict[str, Any]]] = TTLCache(
    maxsize=100, ttl=POSTS_CACHE_TTL
)
content_cache: TTLCache[str, dict[str, Any]] = TTLCache(
    maxsize=50, ttl=CONTENT_CACHE_TTL
)

redis_client: redis.Redis | None = None
redis_url = os.getenv("REDIS_URL")
if redis_url:
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000",
    "Content-Security-Policy": "default-src 'self'",
}

# Current list of posts shown on the index page
filtered_posts: list[dict[str, Any]] = []
current_page: int = 1
posts_per_page: int = 5
search_query: str = ""
active_tags: list[str] = []


@app.middleware("http")
async def apply_security_headers(request: Request, call_next):
    response = await call_next(request)
    for header, value in SECURITY_HEADERS.items():
        response.headers.setdefault(header, value)
    return response


def get_cached_posts() -> list[dict[str, Any]]:
    """Get all posts with caching for improved performance."""
    cache_key = "all_posts"
    if redis_client:
        try:
            data = asyncio.run(redis_client.get(cache_key))
            if data:
                return json.loads(data)
        except Exception:
            logger.exception("Redis get failed for %s", cache_key)
    try:
        return posts_cache[cache_key]
    except KeyError:
        posts = get_all_posts()
        posts_cache[cache_key] = posts
        if redis_client:
            try:
                asyncio.run(
                    redis_client.setex(cache_key, POSTS_CACHE_TTL, json.dumps(posts))
                )
            except Exception:
                logger.exception("Redis set failed for %s", cache_key)
        logger.info(f"Cached {len(posts)} posts")
        return posts


def get_cached_post(slug: str) -> dict[str, Any] | None:
    """Get a single post with caching for improved performance."""
    if redis_client:
        try:
            data = asyncio.run(redis_client.get(slug))
            if data:
                return json.loads(data)
        except Exception:
            logger.exception("Redis get failed for %s", slug)
    if slug in content_cache:
        logger.info(f"Serving post '{slug}' from cache")
        return content_cache[slug]

    post = get_post_by_slug(slug)
    if post:
        content_cache[slug] = post
        if redis_client:
            try:
                asyncio.run(
                    redis_client.setex(slug, CONTENT_CACHE_TTL, json.dumps(post))
                )
            except Exception:
                logger.exception("Redis set failed for %s", slug)
        logger.info(f"Cached post '{slug}'")
    return post


def clear_cache() -> None:
    """Clear all caches - useful for development or content updates."""
    posts_cache.clear()
    content_cache.clear()
    if redis_client:
        try:
            asyncio.run(redis_client.flushdb())
        except Exception:
            logger.exception("Redis flush failed")
    logger.info("All caches cleared")


@app.post("/vitals")
async def vitals_endpoint(request: Request) -> dict[str, str]:
    """Receive Web Vitals metrics from the browser."""
    data = await request.json()
    logger.info("Web vitals: %s", data)
    return {"status": "ok"}


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
        css_file.write_text(css_content, encoding="utf-8")
        logger.info("Generated syntax highlighting CSS: %s", css_file)
    except OSError as e:
        logger.error("Failed to generate syntax CSS: %s", e)


def add_global_styles() -> None:
    """Add global styles and external stylesheets with comprehensive favicon support."""
    ui.dark_mode().enable()
    ui.add_head_html(
        """
        <!-- External Stylesheets -->
        <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css\">
        <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
        <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
        <link href=\"https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..700&family=JetBrains+Mono:ital,wght@0,400..800;1,400..800&display=swap\" rel=\"stylesheet\">
        <link rel=\"stylesheet\" href=\"/static/syntax.css\">
        <link rel=\"stylesheet\" href=\"/static/blog.min.css\">

        <!-- Comprehensive Favicon Support -->
        <link rel=\"icon\" type=\"image/x-icon\" href=\"/static/favicon/favicon.ico\" sizes=\"32x32\">
        <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/static/favicon/favicon-16x16.png\">
        <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/static/favicon/favicon-32x32.png\">
        <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/static/favicon/apple-touch-icon.png\">
        <link rel=\"icon\" type=\"image/png\" sizes=\"192x192\" href=\"/static/favicon/android-chrome-192x192.png\">
        <link rel=\"icon\" type=\"image/png\" sizes=\"512x512\" href=\"/static/favicon/android-chrome-512x512.png\">

        <!-- Meta Tags -->
        <meta name=\"theme-color\" content=\"#713A90\">
        <meta name=\"msapplication-TileColor\" content=\"#713A90\">
        <meta name=\"description\" content=\"A lightning-fast, modern blog built with NiceGUI v2.22.1 and Python 3.13\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <meta name=\"author\" content=\"dunamismax\">

        <!-- Open Graph / Social Media -->
        <meta property=\"og:type\" content=\"website\">
        <meta property=\"og:title\" content=\"NiceGUI Blog - Modern Python Blog\">
        <meta property=\"og:description\" content=\"A lightning-fast blog built with NiceGUI v2.22.1, featuring dark theme, zero database dependencies, and modern UI components\">
        <meta property=\"og:image\" content=\"/static/favicon/android-chrome-512x512.png\">
        <meta name=\"twitter:card\" content=\"summary_large_image\">
        <meta name=\"twitter:title\" content=\"NiceGUI Blog\">
        <meta name=\"twitter:description\" content=\"Modern Python blog with dark theme and lightning-fast performance\">

        <!-- Enhanced JavaScript for scroll-to-top button and performance optimizations -->
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Throttled scroll handler for better performance
            let scrollTimeout;
            function toggleScrollButton() {
                const scrollButton = document.querySelector('.scroll-to-top');
                if (scrollButton) {
                    if (window.scrollY > 300) {
                        scrollButton.classList.add('visible');
                    } else {
                        scrollButton.classList.remove('visible');
                    }
                }
            }

            function throttledScroll() {
                if (!scrollTimeout) {
                    scrollTimeout = requestAnimationFrame(() => {
                        toggleScrollButton();
                        scrollTimeout = null;
                    });
                }
            }

            window.addEventListener('scroll', throttledScroll, { passive: true });
            toggleScrollButton(); // Initial check

            // Enhanced lazy loading with error handling
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.classList.add('loaded');
                            observer.unobserve(img);
                        }
                    });
                }, {
                    rootMargin: '10px'
                });

                document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                    imageObserver.observe(img);

                    // Add error handling for broken images
                    img.addEventListener('error', () => {
                        img.style.display = 'none';
                    });
                });
            }

            // Preload critical resources
            const criticalImages = document.querySelectorAll('img[priority="high"]');
            criticalImages.forEach(img => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.as = 'image';
                link.href = img.src;
                document.head.appendChild(link);
            });

            // Add copy buttons to code blocks
            function addCopyButtons() {
                const codeBlocks = document.querySelectorAll('pre.highlight, .highlight pre, pre:has(code)');
                codeBlocks.forEach(pre => {
                    // Skip if copy button already exists
                    if (pre.querySelector('.copy-button')) return;

                    const button = document.createElement('button');
                    button.className = 'copy-button';
                    button.innerHTML = `
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                    `;
                    button.title = 'Copy code';

                    button.addEventListener('click', async () => {
                        const code = pre.querySelector('code') || pre;
                        const text = code.textContent || code.innerText;

                        try {
                            await navigator.clipboard.writeText(text);
                            button.classList.add('copied');
                            button.innerHTML = `
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <polyline points="20,6 9,17 4,12"></polyline>
                                </svg>
                            `;
                            setTimeout(() => {
                                button.classList.remove('copied');
                                button.innerHTML = `
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                    </svg>
                                `;
                            }, 2000);
                        } catch (err) {
                            console.error('Failed to copy code:', err);
                        }
                    });

                    // Style the pre element to position the button
                    pre.style.position = 'relative';
                    pre.appendChild(button);
                });
            }

            // Initial load
            addCopyButtons();

            // Re-run when content changes (for dynamic content)
            const observer = new MutationObserver(addCopyButtons);
            observer.observe(document.body, { childList: true, subtree: true });
        });
        </script>
    """,
        shared=True,
    )

    ui.add_head_html(
        """
        <script>
        if ('serviceWorker' in navigator) {
          window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/sw.js');
          });
        }
        </script>
        <script src=\"https://unpkg.com/web-vitals@3/dist/web-vitals.iife.js\"></script>
        <script>
        function sendToAnalytics(metric) {
          navigator.sendBeacon('/vitals', JSON.stringify(metric));
        }
        webVitals.getCLS(sendToAnalytics);
        webVitals.getINP(sendToAnalytics);
        webVitals.getLCP(sendToAnalytics);
        </script>
        """,
        shared=True,
    )


def create_header() -> ui.element:
    """Create a reusable header component with improved design and centering."""
    with (
        ui.row().classes(
            "w-full justify-center items-center bg-gradient-header"
        ) as header_container,
        ui.column().classes("max-w-4xl w-full px-4 py-8 items-center text-center"),
        ui.element("header").classes("modern-blog-header"),
    ):
        # Main title with improved styling
        with ui.row().classes("items-center justify-center gap-3 mb-3"):
            ui.icon("article", size="2.5rem").classes("text-purple-accent")
            ui.link("NiceGUI Blog", "/blog", new_tab=False).classes(
                "no-underline text-4xl font-bold transition-all duration-300 hover:scale-105"
            ).style(
                "color: var(--purple-accent); text-shadow: 0 2px 4px rgba(0,0,0,0.3)"
            )

        # Subtitle with better typography
        ui.label("A lightning-fast, modern blog built with NiceGUI v2.22.1").classes(
            "text-xl opacity-90 font-medium text-center max-w-2xl mx-auto"
        ).style("color: var(--text-secondary)")

        # Feature badges
        with ui.row().classes("justify-center gap-2 mt-4 flex-wrap"):
            ui.badge("Python 3.13", color="purple").classes("px-3 py-1")
            ui.badge("Dark Theme", color="purple").classes("px-3 py-1")
            ui.badge("Zero Database", color="purple").classes("px-3 py-1")
    return header_container


def create_footer() -> ui.element:
    """Create a reusable footer component using modern NiceGUI patterns."""
    with (
        ui.row().classes("w-full justify-center mt-auto") as footer_container,
        ui.column().classes("max-w-4xl w-full px-4 items-center"),
        ui.element("footer").classes(
            "text-center mt-12 pt-8 border-t border-gray-300 w-full"
        ),
        ui.row().classes("justify-center items-center gap-1 flex-wrap"),
    ):
        ui.label("© 2025 My Blog. Built with")
        ui.link("NiceGUI", "https://nicegui.io", new_tab=True).classes(
            "font-medium"
        ).style("color: var(--purple-accent)")
        ui.label("and love")
    return footer_container


@ui.refreshable
def create_search_bar() -> ui.element:
    """Create a compact search bar component with reactive filtering."""
    with ui.row().classes("search-container") as search_container:
        search_input = (
            ui.input(
                placeholder="Search posts...", on_change=lambda e: filter_posts(e.value)
            )
            .props("borderless dense standout")
            .classes("modern-search-input w-full")
        )
        search_input.props("prepend-icon=search aria-label=Search posts")
    return search_container


def filter_posts(query: str) -> None:
    """Filter posts based on search query and active tags, then refresh UI."""
    global filtered_posts, current_page, search_query
    current_page = 1  # Reset to first page when filtering
    search_query = query
    posts = get_cached_posts()
    filtered_posts_all = apply_filter(query, posts)
    if active_tags:
        filtered_posts_all = filter_posts_by_tags(active_tags, filtered_posts_all)
    filtered_posts, _ = get_paginated_posts(
        filtered_posts_all, current_page, posts_per_page
    )
    logger.info(
        f"Found {len(filtered_posts_all)} posts matching '{query}', showing page {current_page}"
    )
    render_posts.refresh()
    create_pagination.refresh()


def apply_filter(query: str, posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return posts that match a query in title, summary, or tags."""
    if not query:
        return posts
    q = query.casefold()
    return [
        post
        for post in posts
        if q in post.get("title", "").casefold()
        or q in post.get("summary", "").casefold()
        or any(q in tag.casefold() for tag in post.get("tags", []))
    ]


def filter_posts_by_tag(tag: str, posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return posts that contain a specific tag."""
    t = tag.casefold()
    return [post for post in posts if t in [p.casefold() for p in post.get("tags", [])]]


def filter_posts_by_tags(
    tags: list[str], posts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return posts that contain any of the specified tags."""
    tag_set = {t.casefold() for t in tags}
    if not tag_set:
        return posts
    return [
        post for post in posts if tag_set & {p.casefold() for p in post.get("tags", [])}
    ]


def get_paginated_posts(
    posts: list[dict[str, Any]], page: int, per_page: int
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return paginated posts and pagination info."""
    total_posts = len(posts)
    total_pages = max(1, (total_posts + per_page - 1) // per_page)

    # Ensure page is within valid range
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_posts = posts[start_idx:end_idx]

    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "total_posts": total_posts,
        "posts_per_page": per_page,
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "previous_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
    }

    return paginated_posts, pagination_info


def change_page(new_page: int) -> None:
    """Change to a specific page and refresh the UI."""
    global current_page, filtered_posts
    current_page = new_page

    posts = get_cached_posts()
    filtered_posts_all = apply_filter(search_query, posts)
    if active_tags:
        filtered_posts_all = filter_posts_by_tags(active_tags, filtered_posts_all)
    filtered_posts, _ = get_paginated_posts(
        filtered_posts_all, current_page, posts_per_page
    )

    render_posts.refresh()
    create_pagination.refresh()


@ui.refreshable
def create_pagination() -> ui.element:
    """Create pagination controls for blog posts."""
    posts = get_cached_posts()
    total_posts = len(posts)

    if total_posts <= posts_per_page:
        return ui.element("div")  # No pagination needed

    _, pagination_info = get_paginated_posts(posts, current_page, posts_per_page)

    with ui.row().classes(
        "justify-center items-center gap-2 mt-6"
    ) as pagination_container:
        # Previous button
        if pagination_info["has_previous"]:
            ui.button(
                "← Previous",
                on_click=lambda: change_page(pagination_info["previous_page"]),
            ).props("flat").classes("pagination-btn")

        # Page numbers
        total_pages = pagination_info["total_pages"]
        current = pagination_info["current_page"]

        # Show max 5 page numbers with current page in center when possible
        start_page = max(1, current - 2)
        end_page = min(total_pages, start_page + 4)
        start_page = max(1, end_page - 4)

        if start_page > 1:
            ui.button("1", on_click=lambda: change_page(1)).props("flat").classes(
                "pagination-btn"
            )
            if start_page > 2:
                ui.label("...").classes("pagination-ellipsis")

        for page_num in range(start_page, end_page + 1):
            if page_num == current:
                ui.button(str(page_num)).props("").classes("pagination-btn-active")
            else:
                ui.button(
                    str(page_num), on_click=lambda p=page_num: change_page(p)
                ).props("flat").classes("pagination-btn")

        if end_page < total_pages:
            if end_page < total_pages - 1:
                ui.label("...").classes("pagination-ellipsis")
            ui.button(
                str(total_pages), on_click=lambda: change_page(total_pages)
            ).props("flat").classes("pagination-btn")

        # Next button
        if pagination_info["has_next"]:
            ui.button(
                "Next →", on_click=lambda: change_page(pagination_info["next_page"])
            ).props("flat").classes("pagination-btn")

    # Page info
    with ui.row().classes("justify-center mt-2"):
        ui.label(f"Page {current} of {total_pages} ({total_posts} posts)").classes(
            "text-sm opacity-70"
        )

    return pagination_container


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
                        with ui.row().classes("gap-1 flex-wrap"):
                            for tag in post["tags"][:3]:
                                ui.link(
                                    f"#{tag}", f"/blog?tag={tag}", new_tab=False
                                ).classes("tag-pill text-xs")


def create_scroll_to_top() -> ui.element:
    """Create a floating scroll-to-top button with modern styling."""
    with (
        ui.button(
            icon="keyboard_arrow_up",
            on_click=lambda: ui.run_javascript(
                "window.scrollTo({top: 0, behavior: 'smooth'})"
            ),
        )
        .props("fab glossy")
        .classes("scroll-to-top")
        .style(
            "background-color: var(--purple-accent); color: white; box-shadow: 0 4px 20px rgba(113, 58, 144, 0.3)"
        ) as scroll_btn
    ):
        pass
    return scroll_btn


@ui.page("/")
def index() -> None:
    """Root route that redirects to the blog."""
    ui.navigate.to("/blog")


@ui.page("/blog")
def blog_index(request: Request) -> None:
    """Blog index page displaying all posts with optional tag filter."""
    add_global_styles()

    tag = request.query_params.get("tag", "")
    global active_tags
    active_tags = [tag] if tag else []

    with ui.column().classes("w-full items-center min-h-screen"):
        create_header()

        with (
            ui.row().classes("w-full justify-center flex-grow"),
            ui.column().classes("max-w-4xl w-full px-4"),
        ):
            posts = get_cached_posts()
            if tag:
                posts = filter_posts_by_tag(tag, posts)

            paginated_posts, _ = get_paginated_posts(
                posts, current_page, posts_per_page
            )
            filtered_posts[:] = paginated_posts

            create_search_bar()

            render_posts()
            create_pagination()

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
                    "Back to Blog", on_click=lambda: ui.navigate.to("/blog")
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
            ui.button("Back to Blog", on_click=lambda: ui.navigate.to("/blog")).props(
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
            ui.html(post["content"]).classes("blog-content prose prose-lg")

            # Article footer with tags and sharing
            with ui.row().classes(
                "justify-between items-center mt-8 pt-6 border-t border-gray-300 flex-wrap"
            ):
                if post.get("tags"):
                    with ui.row().classes("items-center gap-2 flex-wrap"):
                        ui.label("Tags:").classes("text-sm font-medium opacity-70")
                        for tag in post["tags"]:
                            ui.link(
                                f"#{tag}", f"/blog?tag={tag}", new_tab=False
                            ).classes("tag-pill text-sm")

                with ui.row().classes("gap-2"):

                    async def do_share() -> None:
                        """Share the current post or copy link to clipboard."""
                        js = (
                            "if (navigator.share && navigator.canShare) {"
                            "  try {"
                            "    await navigator.share({title: document.title, url: window.location.href});"
                            "  } catch (e) {"
                            "    if (e.name !== 'AbortError') {"
                            "      await navigator.clipboard.writeText(window.location.href);"
                            "      return 'copied';"
                            "    }"
                            "  }"
                            "} else {"
                            "  await navigator.clipboard.writeText(window.location.href);"
                            "  return 'copied';"
                            "}"
                        )
                        result = await ui.run_javascript(js)
                        if result == "copied":
                            ui.notify("Link copied to clipboard", type="positive")

                    ui.button("Share", icon="share", on_click=do_share).props(
                        "flat size=sm"
                    ).style("color: var(--orange-accent)")

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
        favicon="static/favicon/favicon.ico",
        dark=True,
    )
