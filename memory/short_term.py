from collections import deque
from typing import Any


class ShortTermMemory:
    """In-process rolling memory for the current assessment session."""

    def __init__(self, maxlen: int = 50):
        self._items: deque[dict[str, Any]] = deque(maxlen=maxlen)

    def add(self, role: str, content: str, **meta: Any) -> None:
        self._items.append({"role": role, "content": content, **meta})

    def recent(self, n: int = 10) -> list[dict[str, Any]]:
        return list(self._items)[-n:]

    def clear(self) -> None:
        self._items.clear()
