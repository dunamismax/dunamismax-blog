"""Tests for content management utilities."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.content import (  # noqa: E402
    create_slug,
    get_all_posts,
    get_post_by_slug,
    validate_post_metadata,
)


def test_create_slug_basic() -> None:
    """Ensure slugs are generated from filenames."""
    assert create_slug("My Post.md") == "my-post"


def test_validate_post_metadata_defaults() -> None:
    """Metadata should fall back to sensible defaults."""
    meta = validate_post_metadata({}, "my_post.md")
    assert meta["title"] == "My Post"


def test_get_all_posts_contains_metrics() -> None:
    """Loaded posts should include content metrics."""
    posts = get_all_posts()
    assert posts, "Expected at least one post"
    first = posts[0]
    assert "word_count" in first and first["word_count"] > 0
    assert "read_time" in first and first["read_time"] >= 1


def test_get_post_by_slug_returns_content() -> None:
    """Posts can be retrieved by slug with HTML content."""
    posts = get_all_posts()
    slug = posts[0]["slug"]
    post = get_post_by_slug(slug)
    assert post is not None
    assert "content" in post and "<" in post["content"]


def test_get_post_by_slug_sanitizes_html(tmp_path: Path) -> None:
    """HTML content should be sanitized to prevent scripts."""
    posts_dir = Path("content/posts")
    test_file = posts_dir / "xss-test.md"
    test_file.write_text(
        "---\ntitle: XSS\n---\n<script>alert('bad')</script>", encoding="utf-8"
    )
    try:
        post = get_post_by_slug("xss-test")
        assert post is not None
        assert "<script>" not in post["content"]
    finally:
        test_file.unlink(missing_ok=True)
