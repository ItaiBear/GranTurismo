from __future__ import annotations

import pygame

from .base import Scene


class TransitionScene(Scene):
    """The 'reset vehicles' speed-up effect from v1: the road accelerates
    until existing cars sweep off-screen, then decelerates back to rest.
    """

    def __init__(self, app, next_factory, accel: int = 2, max_speed: int = 80, decel: int = 1):
        super().__init__(app)
        self._next_factory = next_factory
        self._accel = accel
        self._max = max_speed
        self._decel = decel
        self._slowing = False
        # Use a high local speed instead of overwriting world.speed permanently;
        # we restore world speed to the default at the end.
        self._original_speed = self.world.speed
        self.world.speed = 10

    def update(self) -> None:
        s = self.settings
        self.world.spawn_step(density_scale=3.0, include_cars=False)
        self.world.scroll_step()

        if self.world.speed >= self._max or self._slowing:
            self._slowing = True
            self.world.speed -= self._decel
        else:
            self.world.speed += self._accel

        if self.world.speed <= 0:
            self.world.ai_cars.empty()
            self.world.speed = self._original_speed
            self.app.set_scene(self._next_factory)

    def render(self, screen: pygame.Surface) -> None:
        self.world.render_background(screen)
