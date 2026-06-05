from __future__ import annotations

import os

# Use the dummy video driver so pygame can build Rects without a display.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()

from granturismo.game.collision import rects_collide  # noqa: E402


def r(x, y, w, h):
    return pygame.Rect(x, y, w, h)


def test_far_apart_does_not_collide():
    assert not rects_collide(r(0, 0, 50, 50), r(500, 500, 50, 50))


def test_full_overlap_collides():
    assert rects_collide(r(0, 0, 50, 50), r(10, 10, 50, 50))


def test_one_pixel_overlap_does_not_collide_with_default_inset():
    # Inset is 5 — overlap of 1 pixel on each side is forgiven.
    assert not rects_collide(r(0, 0, 50, 50), r(46, 46, 50, 50))


def test_overlap_beyond_inset_collides():
    # Raw overlap of 15px on each axis → after the 5px inset still 5px → collide.
    assert rects_collide(r(0, 0, 50, 50), r(35, 35, 50, 50))


def test_zero_inset_uses_strict_aabb():
    assert rects_collide(r(0, 0, 50, 50), r(49, 49, 50, 50), shrink=0)
    assert not rects_collide(r(0, 0, 50, 50), r(50, 50, 50, 50), shrink=0)
