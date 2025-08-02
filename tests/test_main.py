"""Tests for main application utilities."""

from typing import Any

from starlette.requests import Request

from app.main import (
    apply_filter,
    filter_posts_by_tag,
    filter_posts_by_tags,
    is_admin_authorized,
)


def make_request(query: str = "") -> Request:
    scope = {
        "type": "http",
        "query_string": query.encode(),
        "headers": [],
    }

    async def receive() -> dict[str, Any]:
        return {"type": "http.request"}

    return Request(scope, receive)


def test_apply_filter_matches_query() -> None:
    posts = [
        {"title": "Python", "summary": "about code", "tags": ["dev"]},
        {"title": "Other", "summary": "misc", "tags": ["misc"]},
    ]
    assert apply_filter("python", posts) == [posts[0]]
    assert apply_filter("", posts) == posts


def test_is_admin_authorized(monkeypatch) -> None:
    monkeypatch.setenv("BLOG_ADMIN_TOKEN", "secret")
    assert is_admin_authorized(make_request("token=secret"))
    assert not is_admin_authorized(make_request("token=bad"))
    monkeypatch.delenv("BLOG_ADMIN_TOKEN", raising=False)
    assert not is_admin_authorized(make_request("token=secret"))


def test_filter_posts_by_tag() -> None:
    posts = [
        {"title": "Python", "tags": ["dev", "python"]},
        {"title": "Other", "tags": ["misc"]},
    ]
    assert filter_posts_by_tag("python", posts) == [posts[0]]
    assert filter_posts_by_tag("unknown", posts) == []


def test_filter_posts_by_tags() -> None:
    posts = [
        {"title": "Python", "tags": ["dev", "python"]},
        {"title": "Misc", "tags": ["misc"]},
        {"title": "PyMisc", "tags": ["python", "misc"]},
    ]
    assert filter_posts_by_tags(["python"], posts) == [posts[0], posts[2]]
    assert filter_posts_by_tags(["dev", "misc"], posts) == [
        posts[0],
        posts[1],
        posts[2],
    ]
    assert filter_posts_by_tags(["unknown"], posts) == []
