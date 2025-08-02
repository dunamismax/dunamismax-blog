---
title: "Boosting NiceGUI Performance with TTLCache"
date: "8/1/2025"
summary: "Speed up repeated NiceGUI computations by storing results in cachetools.TTLCache."
tags: ["nicegui", "cache", "performance", "python", "tutorial"]
---

# Boosting NiceGUI Performance with TTLCache

Caching expensive operations can dramatically improve responsiveness. `TTLCache` from the `cachetools` package stores values for a fixed time-to-live (TTL), automatically expiring stale entries. It is a light‑weight solution that keeps your interface responsive without complicating your code. Even small apps benefit when you avoid repeatedly computing the same result or fetching identical API payloads.

Before reaching for a cache, profile where your application spends time. Operations that hit remote services or render large data sets are excellent candidates. `TTLCache` is thread‑safe and works in async contexts, making it a flexible choice for NiceGUI projects.

## Setting Up a Cache

```python
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)
```

`maxsize` limits the number of cached entries while `ttl` controls how long items remain valid in seconds. Adjust these values based on your data set and refresh rate. You can create multiple caches for different resource types—for example, a short‑lived cache for weather data and a longer TTL for static configuration.

## Using the Cache

```python
def get_data(key: str) -> str:
    if key in cache:
        return cache[key]
    result = expensive_lookup(key)
    cache[key] = result
    return result
```

This pattern keeps frequently accessed data fresh without redoing work. In a NiceGUI application you might cache database queries, API responses, or heavy calculations. Cached functions can be wrapped with `@ui.refreshable` to update the UI when new data arrives.

`cachetools` also provides decorators to simplify caching. The `@cached` decorator transparently handles lookups and storage:

```python
from cachetools import cached

@cached(cache)
def compute(x: int, y: int) -> int:
    return expensive_math(x, y)
```

Decorators make it easy to swap cache implementations later or to apply the same cache across multiple functions.

## Example: Caching API Responses

```python
from nicegui import ui
import httpx

async def fetch_weather(city: str) -> dict:
    if city in cache:
        return cache[city]
    response = await httpx.get(f'https://api.example.com/weather/{city}')
    data = response.json()
    cache[city] = data
    return data

@ui.page('/weather/{city}')
async def weather(city: str) -> None:
    ui.dark_mode().enable()
    info = await fetch_weather(city)
    ui.label(f"Temperature: {info['temp']}")
```

The first request for a city triggers a network call; subsequent visits within the TTL window load instantly from memory.

Handle network errors gracefully by wrapping calls in `try`/`except` blocks and using fallbacks when the cache is empty. Pair the cache with `asyncio.create_task` to refresh data in the background without blocking the UI.

## Invalidation and Debugging

`TTLCache` automatically removes expired entries, but you can also clear specific keys with `del cache[key]` or wipe the entire cache using `cache.clear()`. Logging cache hits and misses helps tune performance and verify that caching behaves as expected. When data changes externally, proactively invalidate affected keys so users see the latest information.

## Conclusion

Strategic caching is one of the quickest ways to improve perceived speed. `TTLCache` keeps your NiceGUI interface snappy while ensuring users always see relatively fresh data. Combine it with async tasks and `ui.notify` to provide responsive feedback when data refreshes. Thoughtful cache policies lead to fewer database hits, lower latency, and happier users.
