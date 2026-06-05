from __future__ import annotations

import random
from typing import Sequence

import pygame

from .entities import AICar, CarModel, Scenery


def try_spawn_ai(
    road,
    cars_group: pygame.sprite.Group,
    models: Sequence[CarModel],
    base_density: int,
    player_height: int,
    spawn_margin: int,
    scroll_speed: int,
) -> AICar | None:
    """Maybe spawn a single AI car. Returns it (not in any group yet) or None.

    Validity rules (corrected from v1):
      - Don't put a new car in the same lane as another that's still near the top.
      - Don't spawn if other cars already cover all-but-one lane at the top
        (would force the player into a roadblock).
    """
    cars = list(cars_group)
    density = base_density
    if len(cars) == 0:
        density //= 4
    elif len(cars) == 1:
        density //= 2
        if cars[0].rect.y > road.window_height // 2 + cars[0].rect.height + spawn_margin * 2:
            density //= 2
    if density <= 0:
        density = 1
    if random.randint(0, density) != 0:
        return None

    model = random.choice(models)
    lane = random.randint(1, road.lane_count)
    x = road.lane_x(lane, model.width)

    danger_zone = player_height + spawn_margin * 2
    top_cars = [c for c in cars if c.rect.y < danger_zone]
    for c in top_cars:
        if abs(c.rect.x - x) < road.lane_width // 2:
            return None
    if len(top_cars) >= road.lane_count - 1:
        return None
    return AICar(model, x, scroll_speed=scroll_speed)


def try_spawn_tree(
    road,
    image: pygame.Surface,
    tree_width: int,
    tree_height: int,
    density: int,
    margin_from_road: int,
    group: pygame.sprite.Group,
) -> Scenery | None:
    if density <= 0 or random.randint(0, density) != 1:
        return None
    x = _off_road_x(road, tree_width, margin_from_road)
    tree = Scenery(image, x, -tree_height)
    group.add(tree)
    return tree


def _off_road_x(road, sprite_width: int, margin_from_road: int) -> int:
    left_lo = -sprite_width
    left_hi = road.road_left - sprite_width - margin_from_road
    right_lo = road.road_right + margin_from_road
    right_hi = road.window_width
    left_ok = left_hi >= left_lo
    right_ok = right_hi >= right_lo
    if left_ok and right_ok:
        return random.randint(left_lo, left_hi) if random.random() < 0.5 else random.randint(right_lo, right_hi)
    if left_ok:
        return random.randint(left_lo, left_hi)
    if right_ok:
        return random.randint(right_lo, right_hi)
    return 0
