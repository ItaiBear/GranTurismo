from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ..app import App


class Scene:
    """Default no-op scene. Override what you need."""

    def __init__(self, app: "App"):
        self.app = app
        self.world = app.world
        self.settings = app.settings
        self.assets = app.assets

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass
