from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Sequence

import pygame


class AssetManager:
    """Loads and caches surfaces, fonts, and music.

    A pygame display must already be initialized before constructing this — we
    call .convert_alpha() on every surface to match the screen's pixel format,
    which is the single biggest blit-speed win we get for free.
    """

    def __init__(self, root: str | Path = "."):
        self.root = Path(root)
        self._surface_cache: dict[tuple[str, tuple | None], pygame.Surface] = {}

    def surface(
        self, relative_path: str, transparent: Sequence[int] | None = None
    ) -> pygame.Surface:
        key = (relative_path, tuple(transparent) if transparent else None)
        cached = self._surface_cache.get(key)
        if cached is not None:
            return cached
        path = self.root / relative_path
        image = pygame.image.load(str(path))
        if transparent is not None:
            image = image.convert()
            image.set_colorkey(tuple(transparent))
        else:
            image = image.convert_alpha()
        self._surface_cache[key] = image
        return image

    @lru_cache(maxsize=64)
    def font(self, name: str, size: int, bold: bool = False, italic: bool = False) -> pygame.font.Font:
        return pygame.font.SysFont(name, size, bold, italic)

    def play_music(self, relative_path: str, volume: float, loop: bool = True) -> None:
        pygame.mixer.music.load(str(self.root / relative_path))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
