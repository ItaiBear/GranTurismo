from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pygame


def _to_ns(value: Any) -> Any:
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _to_ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_to_ns(v) for v in value]
    return value


class Settings(SimpleNamespace):
    """Attribute-access view over config.json with a few convenience helpers."""

    @classmethod
    def load(cls, path: str | Path = "config.json") -> "Settings":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        ns = _to_ns(data)
        return cls(**ns.__dict__)

    def key(self, name: str) -> int:
        """Translate a key-binding name from config into a pygame key constant."""
        raw = getattr(self.keys, name)
        return _KEY_ALIASES.get(raw.lower(), pygame.key.key_code(raw))


_KEY_ALIASES = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "space": pygame.K_SPACE,
    "enter": pygame.K_RETURN,
    "return": pygame.K_RETURN,
    "escape": pygame.K_ESCAPE,
    "esc": pygame.K_ESCAPE,
    "backspace": pygame.K_BACKSPACE,
    "tab": pygame.K_TAB,
    "+": pygame.K_PLUS,
    "-": pygame.K_MINUS,
}
