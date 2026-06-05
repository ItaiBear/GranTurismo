from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class CarModel:
    image: pygame.Surface
    width: int
    height: int


class Player(pygame.sprite.Sprite):
    """Yellow car the user controls. Y is fixed once at rest; the world scrolls past it."""

    def __init__(self, model: CarModel, road, starting_lane: int, horizontal_speed: int):
        super().__init__()
        self.image = model.image
        self.rect = self.image.get_rect()
        self.road = road
        self.target_lane = starting_lane
        self.horizontal_speed = horizontal_speed
        self.rect.x = road.lane_x(starting_lane, self.rect.width)

    def shift(self, direction: int) -> None:
        new_lane = self.target_lane + direction
        if 1 <= new_lane <= self.road.lane_count:
            self.target_lane = new_lane

    def update(self) -> None:
        target_x = self.road.lane_x(self.target_lane, self.rect.width)
        dx = target_x - self.rect.x
        if abs(dx) <= self.horizontal_speed:
            self.rect.x = target_x
        else:
            self.rect.x += self.horizontal_speed if dx > 0 else -self.horizontal_speed


class AICar(pygame.sprite.Sprite):
    """Computer-controlled car. Moves down at (player_speed - own_scroll_speed)."""

    def __init__(self, model: CarModel, x: int, scroll_speed: int):
        super().__init__()
        self.image = model.image
        self.rect = self.image.get_rect(topleft=(x, -model.height))
        self.scroll_speed = scroll_speed

    def update(self, player_speed: float, window_height: int) -> None:
        self.rect.y += int(player_speed - self.scroll_speed)
        if self.rect.top >= window_height:
            self.kill()


class Scenery(pygame.sprite.Sprite):
    """Trees and cows — pure decoration, scroll down at the player's speed."""

    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed: float, window_height: int) -> None:
        self.rect.y += int(speed)
        if self.rect.top >= window_height:
            self.kill()
