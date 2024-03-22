from typing import Any


class LRUCache:
    """A class representing an LRU cache."""

    def __init__(self, capacity: int = 10) -> None:
        self.cache: dict[str, Any] = {}
        self.keys: list[str] = []
        self.capacity = capacity

    def get(self, key: str) -> Any:  # noqa: ANN401
        """Get a value from the cache and mark as most recently used."""
        if key in self.cache:
            # Move the key to the end to mark it as most recently used
            self.keys.remove(key)
            self.keys.append(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set a value in the cache and handle capacity."""
        if key in self.cache:
            # Move the key to the end to mark it as most recently used
            self.keys.remove(key)
        elif len(self.keys) >= self.capacity:
            lru_key = self.keys.pop(0)  # Remove and return the least recently used key
            del self.cache[lru_key]  # Remove the least recently used item from the cache

        # Add the new key and value to the cache and mark as most recently used
        self.cache[key] = value
        self.keys.append(key)
