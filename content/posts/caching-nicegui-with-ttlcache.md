---
title: "Boosting NiceGUI Performance with TTLCache"
date: "8/1/2025"
summary: "Speed up repeated NiceGUI computations by storing results in cachetools.TTLCache."
tags: ["nicegui", "cache", "performance", "python", "tutorial"]
---

# Boosting NiceGUI Performance with TTLCache

Caching expensive operations can dramatically improve responsiveness. `TTLCache` from the `cachetools` package stores values for a fixed time-to-live (TTL), automatically expiring stale entries. It is a light‑weight solution that keeps your interface responsive without complicating your code.

## Setting Up a Cache

```python
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)
```

`maxsize` limits the number of cached entries while `ttl` controls how long items remain valid in seconds. Adjust these values based on your data set and refresh rate.

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

## Invalidation and Debugging

`TTLCache` automatically removes expired entries, but you can also clear specific keys with `del cache[key]` or wipe the entire cache using `cache.clear()`. Logging cache hits and misses helps tune performance and verify that caching behaves as expected.

## Conclusion

Strategic caching is one of the quickest ways to improve perceived speed. `TTLCache` keeps your NiceGUI interface snappy while ensuring users always see relatively fresh data. Combine it with async tasks and `ui.notify` to provide responsive feedback when data refreshes.
