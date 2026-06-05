from __future__ import annotations

import pygame

from .base import Scene


class PauseScene(Scene):
    """Modal pause overlay. Renders a snapshot of the previous frame under a
    white veil and resumes the previous scene on the next key/click.
    """

    def __init__(self, app, return_to: Scene):
        super().__init__(app)
        self._return_to = return_to
        self._backdrop = app.screen.copy()
        win = self.settings.window
        veil = pygame.Surface((win.width, win.height))
        veil.set_alpha(128)
        veil.fill((255, 255, 255))
        self._backdrop.blit(veil, (0, 0))
        font = self.assets.font("Calibri", 50, True)
        label = font.render("Press any key to continue", True, (0, 0, 0))
        self._backdrop.blit(label, label.get_rect(center=(win.width // 2, win.height // 2)))
        pygame.mixer.music.pause()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            pygame.mixer.music.unpause()
            self.app.scene = self._return_to

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self._backdrop, (0, 0))
