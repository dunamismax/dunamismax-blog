"""Tests for main application utilities."""

from typing import Any

from starlette.requests import Request

from app.main import apply_filter, is_admin_authorized


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
