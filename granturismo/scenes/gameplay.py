from __future__ import annotations

import pygame

from ..game.collision import rects_collide
from .base import Scene


class GameplayScene(Scene):
    """The active race. Player dodges AI cars; score accumulates with speed."""

    def __init__(self, app):
        super().__init__(app)
        win = self.settings.window
        self.world.speed = 0  # ramps up to default in first ~speed frames
        self.score = 0
        self._start_ticks = pygame.time.get_ticks()

        # GO sign sliding down after countdown
        trans = tuple(self.settings.ui_assets.countdown_transparent)
        self._go_sign = self.assets.surface(self.settings.ui_assets.go, transparent=trans)
        self._go_pos = [win.width // 2 - 50, int(win.height * 0.25)]

        self._pause_icon = self.assets.surface(self.settings.ui_assets.pause, transparent=trans)
        self._mute_icon = self.assets.surface(self.settings.ui_assets.mute)
        self._unmute_icon = self.assets.surface(self.settings.ui_assets.unmute)
        self._pause_icon_rect = pygame.Rect(10, 10, 50, 50)
        self._mute_icon_rect = pygame.Rect(60, 10, 40, 40)

        self._score_font = self.assets.font("Comic Sans MS", 47, True)

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
            if event.key == self.settings.key("left"):
                self.world.player.shift(-1)
            elif event.key == self.settings.key("right"):
                self.world.player.shift(+1)
            elif event.key == self.settings.key("pause"):
                self._enter_pause()
            elif event.key == self.settings.key("mute"):
                self.world.toggle_mute()

    def update(self) -> None:
        s = self.settings
        # ramp up speed to default at the start
        if self.world.speed < s.player.speed:
            self.world.speed += 1

        # difficulty: every speedup_seconds, +1 speed
        elapsed = (pygame.time.get_ticks() - self._start_ticks) / 1000.0
        if elapsed > s.difficulty.speedup_seconds:
            self._start_ticks = pygame.time.get_ticks()
            self.world.speed += s.difficulty.speedup_amount

        self.world.spawn_step()
        self.world.scroll_step()
        if self.world.player is not None:
            self.world.player.update()

        # Slide GO sign off-screen
        if self._go_pos[1] < self.settings.window.height:
            self._go_pos[1] += int(self.world.speed)

        # Collision
        player = self.world.player
        if player is not None:
            for car in self.world.ai_cars:
                if rects_collide(player.rect, car.rect):
                    from .game_over import GameOverScene

                    self.app.set_scene(GameOverScene, score=self.score)
                    return

        self.score += int(self.world.speed)

    def render(self, screen: pygame.Surface) -> None:
        self.world.render_world(screen)
        if self._go_pos[1] < self.settings.window.height:
            screen.blit(self._go_sign, self._go_pos)
        self.world.render_player(screen)
        self._render_score(screen)
        screen.blit(self._pause_icon, self._pause_icon_rect)
        screen.blit(self._mute_icon if self.world.muted else self._unmute_icon, self._mute_icon_rect)

    def _render_score(self, screen: pygame.Surface) -> None:
        from ..ui.widgets import make_round_panel

        text = str(self.score)
        win = self.settings.window
        theme = self.settings.theme
        box_w = 35 * len(text) + 40
        box_h = 65
        box_x = win.width - 30 * len(text) - 35
        box_y = 6
        bg = make_round_panel((box_w, box_h), (255, 255, 255), 15, alpha=90)
        screen.blit(bg, (box_x, box_y))
        label = self._score_font.render(text, True, tuple(theme.button_primary))
        screen.blit(label, label.get_rect(center=(box_x + box_w // 2 - 10, box_y + box_h // 2 - 2)))
