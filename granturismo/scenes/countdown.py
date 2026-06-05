from __future__ import annotations

import pygame

from .base import Scene


class CountdownScene(Scene):
    """3-2-1 then immediately into gameplay.

    Timing matches v1:
      * counter 0: no sign — player drives in
      * counter 1: sign_3
      * counter 2: sign_2
      * counter 3: sign_1
      * counter 4: switch to GameplayScene (which renders GO sliding down)
    """

    def __init__(self, app):
        super().__init__(app)
        win = self.settings.window
        self.world.ai_cars.empty()
        self.world.speed = 0
        self.player = self.world.reset_player(
            start_y=win.height,
            lane=(self.settings.road.lane_count + 1) // 2,
        )
        self._rest_y_threshold = int(win.height * self.settings.player.rest_y_ratio)
        self._brake_y_threshold = int(win.height * self.settings.player.brake_y_ratio)
        self._temp_speed = 1
        self._counter = 0
        self._start_ticks = pygame.time.get_ticks()

        trans = tuple(self.settings.ui_assets.countdown_transparent)
        self._signs = {
            1: self.assets.surface(self.settings.ui_assets.countdown_3, transparent=trans),
            2: self.assets.surface(self.settings.ui_assets.countdown_2, transparent=trans),
            3: self.assets.surface(self.settings.ui_assets.countdown_1, transparent=trans),
        }
        self._sign_pos = (win.width // 2 - 50, int(win.height * 0.25))

        self._pause_icon = self.assets.surface(self.settings.ui_assets.pause, transparent=trans)
        self._mute_icon = self.assets.surface(self.settings.ui_assets.mute)
        self._unmute_icon = self.assets.surface(self.settings.ui_assets.unmute)
        self._pause_icon_rect = pygame.Rect(10, 10, 50, 50)
        self._mute_icon_rect = pygame.Rect(60, 10, 40, 40)

    def _enter_pause(self) -> None:
        from .pause import PauseScene

        self.app.set_scene(PauseScene, return_to=self)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._pause_icon_rect.collidepoint(event.pos):
                self._enter_pause()
            elif self._mute_icon_rect.collidepoint(event.pos):
                self.world.toggle_mute()
        elif event.type == pygame.KEYDOWN:
            if event.key == self.settings.key("pause"):
                self._enter_pause()
            elif event.key == self.settings.key("mute"):
                self.world.toggle_mute()

    def update(self) -> None:
        self.world.spawn_step(include_cars=False)
        self.world.scroll_step()

        if self.player.rect.y > self._rest_y_threshold:
            if self.player.rect.y < self._brake_y_threshold:
                self._temp_speed -= 2
            self.player.rect.y -= self._temp_speed
            self._temp_speed += 1

        if (pygame.time.get_ticks() - self._start_ticks) / 1000.0 > 1.0:
            self._start_ticks = pygame.time.get_ticks()
            self._counter += 1
        if self._counter >= 4:
            from .gameplay import GameplayScene

            self.app.set_scene(GameplayScene)

    def render(self, screen: pygame.Surface) -> None:
        self.world.render_world(screen)
        sign = self._signs.get(self._counter)
        if sign is not None:
            screen.blit(sign, self._sign_pos)
        self.world.render_player(screen)
        screen.blit(self._pause_icon, self._pause_icon_rect)
        screen.blit(self._mute_icon if self.world.muted else self._unmute_icon, self._mute_icon_rect)
