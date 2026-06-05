from __future__ import annotations

import os
import random
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()
pygame.display.set_mode((1, 1))

from granturismo.game.entities import AICar, CarModel  # noqa: E402
from granturismo.game.road import Road  # noqa: E402
from granturismo.game.spawner import try_spawn_ai  # noqa: E402


def make_settings():
    return SimpleNamespace(
        window=SimpleNamespace(width=1300, height=700),
        road=SimpleNamespace(
            lane_width=130,
            lane_count=3,
            background_color=[0, 130, 0],
            lane_color=[71, 71, 64],
            lines_color=[255, 255, 255],
            lines_height=70,
            lines_width=10,
            lines_margin=80,
            side_lines_height=90,
            side_lines_width=10,
            side_lines_colors=[[237, 28, 36], [255, 255, 255]],
        ),
    )


def make_model():
    surf = pygame.Surface((70, 137))
    return CarModel(surf, 70, 137)


def test_spawner_returns_none_when_density_misses(monkeypatch):
    random.seed(0)
    road = Road(make_settings())
    group = pygame.sprite.Group()
    # density=1000 with empty list → divided by 4 → 250; randint(0,250) is mostly nonzero
    misses = sum(
        try_spawn_ai(road, group, [make_model()], 1000, 137, 30, scroll_speed=7) is None
        for _ in range(50)
    )
    assert misses >= 40  # vast majority should miss


def test_spawner_does_not_overlap_same_lane(monkeypatch):
    random.seed(1)
    road = Road(make_settings())
    group = pygame.sprite.Group()
    # Plant a car near the top in lane 2
    model = make_model()
    lane2_x = road.lane_x(2, model.width)
    occupant = AICar(model, lane2_x, scroll_speed=7)
    occupant.rect.y = 50
    group.add(occupant)

    # Force a spawn attempt every call by patching randint(0, density) to return 0
    monkeypatch.setattr(
        "granturismo.game.spawner.random.randint",
        lambda lo, hi: 0 if (lo == 0 and hi != 0) else 2,
    )

    # 'lane' choice = randint(1, 3); make it return 2 → same lane → must refuse
    monkeypatch.setattr("granturismo.game.spawner.random.choice", lambda seq: seq[0])

    # Now force lane 2 selection: randint(1, lane_count) = 2
    # Our patch returns 0 for randint(0, density), but lane uses randint(1, 3).
    # Refine the patch:
    def patched_randint(lo, hi):
        if lo == 0:
            return 0  # always trigger
        return 2  # always pick lane 2

    monkeypatch.setattr("granturismo.game.spawner.random.randint", patched_randint)

    new = try_spawn_ai(road, group, [model], 4, 137, 30, scroll_speed=7)
    assert new is None  # because lane 2 is already taken at the top


def test_spawner_refuses_roadblock_situation(monkeypatch):
    random.seed(2)
    road = Road(make_settings())
    group = pygame.sprite.Group()
    model = make_model()
    # Two cars near top — in lanes 1 and 2; trying to add a third would block lane 3 too
    for lane in (1, 2):
        car = AICar(model, road.lane_x(lane, model.width), scroll_speed=7)
        car.rect.y = 40
        group.add(car)

    def patched_randint(lo, hi):
        if lo == 0:
            return 0
        return 3  # pick lane 3

    monkeypatch.setattr("granturismo.game.spawner.random.randint", patched_randint)
    monkeypatch.setattr("granturismo.game.spawner.random.choice", lambda seq: seq[0])

    new = try_spawn_ai(road, group, [model], 4, 137, 30, scroll_speed=7)
    # With 2 cars in the danger zone and lane_count=3, len(top_cars) >= lane_count - 1 → refuse
    assert new is None
