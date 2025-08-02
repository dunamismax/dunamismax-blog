---
title: "Boosting NiceGUI Performance with TTLCache"
date: "8/1/2025"
summary: "Use cachetools.TTLCache to speed up repeated computations in NiceGUI apps."
tags: ["nicegui", "cache", "performance", "python", "tutorial"]
---

# Boosting NiceGUI Performance with TTLCache

Caching expensive operations can dramatically improve responsiveness.

## Setting Up a Cache

```python
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)
```

## Using the Cache

```python
def get_data(key: str) -> str:
    if key in cache:
        return cache[key]
    result = expensive_lookup(key)
    cache[key] = result
    return result
```

This pattern keeps frequently accessed data fresh without redoing work.
