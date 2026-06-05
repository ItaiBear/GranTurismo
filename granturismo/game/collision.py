from __future__ import annotations

import pygame


def rects_collide(a: pygame.Rect, b: pygame.Rect, shrink: int = 5) -> bool:
    """Axis-aligned bounding-box collision with a small inset.

    The inset matches the v1 game's "forgiving" hit boxes — the bumpers can
    overlap by a few pixels before counting as a crash.
    """
    if shrink == 0:
        return a.colliderect(b)
    return a.inflate(-2 * shrink, -2 * shrink).colliderect(b.inflate(-2 * shrink, -2 * shrink))
