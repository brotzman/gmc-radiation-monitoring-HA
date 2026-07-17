from __future__ import annotations

import copy
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Hashable
from typing import Any, TypeVar

T = TypeVar("T")


class RevisionCache:
    """Small thread-safe LRU cache for immutable analysis snapshots."""

    def __init__(self, *, max_entries: int = 12, ttl_seconds: float = 300.0) -> None:
        self.max_entries = max(1, int(max_entries))
        self.ttl_seconds = max(1.0, float(ttl_seconds))
        self._lock = threading.Lock()
        self._items: OrderedDict[Hashable, tuple[float, Any]] = OrderedDict()

    def get_or_build(self, key: Hashable, builder: Callable[[], T]) -> T:
        now = time.monotonic()
        with self._lock:
            item = self._items.get(key)
            if item is not None and now - item[0] <= self.ttl_seconds:
                self._items.move_to_end(key)
                return copy.deepcopy(item[1])
            if item is not None:
                self._items.pop(key, None)
        value = builder()
        with self._lock:
            self._items[key] = (now, copy.deepcopy(value))
            self._items.move_to_end(key)
            while len(self._items) > self.max_entries:
                self._items.popitem(last=False)
        return value

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
