from __future__ import annotations

import pygame

from ..ui.widgets import SlidingPanel, make_round_panel
from .base import Scene


class MainMenuScene(Scene):
    """Title screen with a sliding panel containing the logo and Play Now button.

    The road continues to scroll and AI cars continue spawning behind the panel —
    we never tear down the World between scenes.
    """

    def __init__(self, app):
        super().__init__(app)
        self._build_layout()
        self._start_ticks = pygame.time.get_ticks()
        self._play_pressed = False

    def _build_layout(self) -> None:
        win = self.settings.window
        theme = self.settings.theme

        panel_w = win.width // 2
        panel_h = int(win.height / 1.4)
        self.panel_size = (panel_w, panel_h)
        panel_bg = make_round_panel(self.panel_size, tuple(theme.panel_bg), 25, alpha=theme.panel_outer_alpha)
        self.panel = SlidingPanel(self.panel_size, win.width // 2, win.height // 2, background=panel_bg, initial_speed=50.0)

        # Play Now button (rendered once)
        margin = 30
        bw = int(panel_w * 0.44)
        bh = int(panel_h * 0.25 - margin * 1.5)
        self.button_size = (bw, bh)
        button_font = self.assets.font("Calibri", 40, True)
        self.button_surface = make_round_panel((bw, bh), tuple(theme.button_primary), 35)
        play_label = button_font.render("Play Now", True, tuple(theme.button_text))
        self.button_surface.blit(play_label, play_label.get_rect(center=(bw // 2, bh // 2)))
        self.button_offset_from_center = (-bw // 2, margin * 2)

        # Logo
        self.logo = self.assets.surface(self.settings.ui_assets.logo)
        self.logo_offset_from_center = (-150, -200)

        # Credit
        credit_font = self.assets.font("Calibri", 20, True, True)
        self.credit_surface = credit_font.render(
            "Created and Designed by Itai Bear, May 2020", True, tuple(theme.text_dark)
        )
        self.credit_y_offset = margin * 2 + bh + 50

        # Mute toggle area
        self.mute_icon = self.assets.surface(self.settings.ui_assets.mute)
        self.unmute_icon = self.assets.surface(self.settings.ui_assets.unmute)
        self.mute_icon_rect = pygame.Rect(60, 10, 40, 40)

    def _button_rect(self) -> pygame.Rect:
        cx = self.panel.center_x + self.button_offset_from_center[0]
        cy = int(self.panel.center_y) + self.button_offset_from_center[1]
        return pygame.Rect(cx, cy, *self.button_size)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            if self._button_rect().collidepoint(pos) and self.panel.is_idle:
                self.panel.slide_out_down()
                self._play_pressed = True
            elif self.mute_icon_rect.collidepoint(pos):
                self.world.toggle_mute()
        elif event.type == pygame.KEYDOWN:
            if event.key == self.settings.key("mute"):
                self.world.toggle_mute()
            elif event.key == self.settings.key("reset_speed"):
                self.world.speed = self.settings.player.speed
            elif event.key == self.settings.key("volume_up"):
                self.world.set_volume(self.world.volume + 0.1)
            elif event.key == self.settings.key("volume_down"):
                self.world.set_volume(self.world.volume - 0.1)

    def update(self) -> None:
        # World keeps scrolling behind the panel.
        self.world.spawn_step()
        self.world.scroll_step()

        # Difficulty ramp: speed up every N seconds while on the menu.
        elapsed = (pygame.time.get_ticks() - self._start_ticks) / 1000.0
        if elapsed > self.settings.difficulty.menu_speedup_seconds:
            self._start_ticks = pygame.time.get_ticks()
            self.world.speed += self.settings.difficulty.speedup_amount

        self.panel.update(self.settings.window.height)

        if self.panel.is_done and self._play_pressed:
            from .transition import TransitionScene
            from .countdown import CountdownScene

            self.app.set_scene(TransitionScene, next_factory=CountdownScene)

    def render(self, screen: pygame.Surface) -> None:
        self.world.render_background(screen)
        self.panel.render(screen)

        if not self.panel.is_done:
            cx = self.panel.center_x
            cy = int(self.panel.center_y)
            screen.blit(self.logo, (cx + self.logo_offset_from_center[0], cy + self.logo_offset_from_center[1]))
            btn_rect = self._button_rect()
            screen.blit(self.button_surface, btn_rect)
            credit_rect = self.credit_surface.get_rect(center=(cx, cy + self.credit_y_offset - self.panel_size[1] // 2 + self.panel_size[1] // 2))
            credit_rect.center = (cx, btn_rect.bottom + 50)
            screen.blit(self.credit_surface, credit_rect)

        icon = self.mute_icon if self.world.muted else self.unmute_icon
        screen.blit(icon, self.mute_icon_rect)
