from __future__ import annotations

from typing import Iterable

import pygame


def make_round_panel(
    size: tuple[int, int],
    color: Iterable[int],
    radius: int,
    alpha: int | None = None,
) -> pygame.Surface:
    """Build a transparent surface with a single rounded-rect fill.

    The result is pre-rendered once per UI element and blitted each frame —
    we never re-tessellate the rounded corners during the game loop.
    """
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rgb = tuple(color)
    fill = (*rgb[:3], alpha) if alpha is not None and len(rgb) == 3 else rgb
    pygame.draw.rect(surf, fill, surf.get_rect(), border_radius=radius)
    return surf


class Label:
    """Static piece of pre-rendered text. Build once, blit forever."""

    __slots__ = ("surface", "rect")

    def __init__(self, surface: pygame.Surface, rect: pygame.Rect):
        self.surface = surface
        self.rect = rect

    @classmethod
    def make(
        cls,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        *,
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> "Label":
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center is not None:
            rect.center = center
        elif topleft is not None:
            rect.topleft = topleft
        return cls(surface, rect)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class SlidingPanel:
    """V1's bouncy top-down menu panel: gravity-driven slide-in with a brief overshoot,
    plus straight exits up or down. Caller pre-renders the panel background once.
    """

    IDLE = 0
    SLIDING_IN = 1
    EXITING_DOWN = 2
    EXITING_UP = 3
    DONE = -1

    def __init__(
        self,
        size: tuple[int, int],
        center_x: int,
        target_y: int,
        background: pygame.Surface,
        initial_speed: float = 50.0,
    ):
        self.size = size
        self.center_x = center_x
        self.target_y = target_y
        self.center_y = -size[1] // 2
        self.speed = initial_speed
        self.state = self.SLIDING_IN
        self.background = background

    def slide_out_down(self) -> None:
        self.state = self.EXITING_DOWN
        self.speed = 10.0

    def slide_out_up(self) -> None:
        self.state = self.EXITING_UP
        self.speed = 10.0

    def update(self, window_height: int) -> None:
        if self.state == self.SLIDING_IN:
            self.center_y += self.speed
            self.speed -= 1
            if self.center_y >= self.target_y - 100:
                self.speed -= 1
            if self.center_y >= self.target_y:
                self.speed -= 5
            if self.center_y >= self.target_y + 100:
                self.speed -= 3
            if self.center_y <= self.target_y + 15 and self.speed < 0:
                self.state = self.IDLE
                self.speed = 0
                self.center_y = self.target_y
        elif self.state == self.EXITING_DOWN:
            self.center_y += self.speed
            self.speed += 3
            if self.center_y - self.size[1] // 2 >= window_height:
                self.state = self.DONE
        elif self.state == self.EXITING_UP:
            self.center_y -= self.speed
            self.speed += 3
            if self.center_y + self.size[1] // 2 <= 0:
                self.state = self.DONE

    @property
    def topleft(self) -> tuple[int, int]:
        return (self.center_x - self.size[0] // 2, int(self.center_y) - self.size[1] // 2)

    @property
    def is_idle(self) -> bool:
        return self.state == self.IDLE

    @property
    def is_done(self) -> bool:
        return self.state == self.DONE

    def render(self, screen: pygame.Surface) -> None:
        if self.state == self.DONE:
            return
        screen.blit(self.background, self.topleft)


class Button:
    """Pre-rendered button (background + text). Hit-test with .contains(pos)."""

    __slots__ = ("rect", "surface")

    def __init__(
        self,
        rect: tuple[int, int, int, int],
        text: str,
        font: pygame.font.Font,
        color: Iterable[int],
        text_color: tuple,
        radius: int = 20,
    ):
        self.rect = pygame.Rect(rect)
        self.surface = make_round_panel(self.rect.size, color, radius)
        label = font.render(text, True, text_color)
        self.surface.blit(label, label.get_rect(center=(self.rect.width // 2, self.rect.height // 2)))

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)

    def contains(self, point: tuple[int, int]) -> bool:
        return self.rect.collidepoint(point)
