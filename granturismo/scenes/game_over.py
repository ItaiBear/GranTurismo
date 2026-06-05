from __future__ import annotations

import pygame

from ..game.entities import AICar, CarModel
from ..ui.widgets import SlidingPanel, make_round_panel
from .base import Scene


class GameOverScene(Scene):
    """End-of-run panel: leaderboard, your score, name entry if ranked, and
    Play Again / Main Menu buttons.
    """

    def __init__(self, app, score: int):
        super().__init__(app)
        self.score = score
        self.name = "_" * self.settings.leaderboard.name_max_length
        self.rank = self.app.leaderboard.submit(score, self.name)

        self._build_layout()
        self._next_scene_factory = None

    # ---------- layout ----------

    def _build_layout(self) -> None:
        win = self.settings.window
        theme = self.settings.theme

        panel_w = win.width // 2
        panel_h = int(win.height / 1.4)
        self.panel_size = (panel_w, panel_h)
        panel_bg = make_round_panel(self.panel_size, tuple(theme.panel_bg), 25, alpha=theme.panel_outer_alpha)
        self.panel = SlidingPanel(self.panel_size, win.width // 2, win.height // 2, panel_bg, initial_speed=50.0)

        margin = 30
        # Leaderboard box (left side)
        lb_w = int(panel_w * 0.45 - margin * 1.5)
        lb_h = panel_h - margin * 2
        self.lb_offset = (margin - panel_w // 2, margin - panel_h // 2)  # from panel center
        self.lb_size = (lb_w, lb_h)
        self.lb_bg = make_round_panel(self.lb_size, tuple(theme.panel_inner), 20, alpha=theme.panel_inner_alpha)

        # Score box (right top)
        sb_w = int(panel_w * 0.55 - margin * 1.5)
        sb_h = int(panel_h * 0.4 - margin)
        self.score_offset = (
            self.lb_offset[0] + lb_w + margin,
            self.lb_offset[1],
        )
        self.score_size = (sb_w, sb_h)
        self.score_bg = make_round_panel(self.score_size, tuple(theme.panel_inner), 20, alpha=theme.panel_inner_alpha)

        # Play Again button
        pa_h = int(panel_h * 0.3 - margin * 1.5)
        self.pa_offset = (self.score_offset[0], self.score_offset[1] + sb_h + margin)
        self.pa_size = (sb_w, pa_h)
        button_font = self.assets.font("Calibri", 45, True)
        self.pa_surface = make_round_panel(self.pa_size, tuple(theme.button_primary), 20)
        pa_label = button_font.render("Play Again", True, tuple(theme.button_text))
        self.pa_surface.blit(pa_label, pa_label.get_rect(center=(sb_w // 2, pa_h // 2)))

        # Main Menu button
        mm_h = pa_h
        self.mm_offset = (self.pa_offset[0], self.pa_offset[1] + pa_h + margin)
        self.mm_size = (sb_w, mm_h)
        self.mm_surface = make_round_panel(self.mm_size, tuple(theme.button_primary), 20)
        mm_label = button_font.render("Main Menu", True, tuple(theme.button_text))
        self.mm_surface.blit(mm_label, mm_label.get_rect(center=(sb_w // 2, mm_h // 2)))

        # Reset leaderboard icon (small)
        self.reset_icon = self.assets.surface(self.settings.ui_assets.reset)
        self.reset_offset = (self.lb_offset[0] + lb_w - 45, self.lb_offset[1] + 15)
        self.reset_size = (self.reset_icon.get_width(), self.reset_icon.get_height())

        # Static labels
        self.lb_title_font = self.assets.font("Calibri", 30, True)
        self.lb_entry_font = self.assets.font("Calibri", 20, True)
        self.score_big_font = self.assets.font("Calibri", 70, True)
        self.rank_score_font = self.assets.font("Calibri", 35, True)
        self.hint_font = self.assets.font("Calibri", 14, True)

        # Mute icons
        self.mute_icon = self.assets.surface(self.settings.ui_assets.mute)
        self.unmute_icon = self.assets.surface(self.settings.ui_assets.unmute)
        self.mute_icon_rect = pygame.Rect(60, 10, 40, 40)

    # ---------- rect helpers (computed each frame relative to current panel position) ----------

    def _abs_rect(self, offset: tuple[int, int], size: tuple[int, int]) -> pygame.Rect:
        cx = self.panel.center_x
        cy = int(self.panel.center_y)
        return pygame.Rect(cx + offset[0], cy + offset[1], size[0], size[1])

    # ---------- event handling ----------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if self.rank is not None and self.panel.is_idle:
                self._handle_name_key(event)
            if event.key == self.settings.key("submit"):
                self._go_to_play_again()
            elif event.key == self.settings.key("mute"):
                self.world.toggle_mute()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not self.panel.is_idle:
                return
            pos = event.pos
            if self._abs_rect(self.pa_offset, self.pa_size).collidepoint(pos):
                self._go_to_play_again()
            elif self._abs_rect(self.mm_offset, self.mm_size).collidepoint(pos):
                self._go_to_main_menu()
            elif self._abs_rect(self.reset_offset, self.reset_size).collidepoint(pos):
                self.app.leaderboard.reset()
                # Re-submit our score after the reset
                self.rank = self.app.leaderboard.submit(self.score, self.name)
            elif self.mute_icon_rect.collidepoint(pos):
                self.world.toggle_mute()

    def _handle_name_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_BACKSPACE:
            for i in range(len(self.name) - 1, -1, -1):
                if self.name[i] != "_":
                    self.name = self.name[:i] + "_" + self.name[i + 1 :]
                    self.app.leaderboard.rename(self.rank, self.name.replace("_", ""))
                    break
        elif event.unicode and event.unicode.isalpha() and "_" in self.name:
            idx = self.name.index("_")
            self.name = self.name[:idx] + event.unicode + self.name[idx + 1 :]
            self.app.leaderboard.rename(self.rank, self.name.replace("_", ""))

    # ---------- transitions ----------

    def _go_to_play_again(self) -> None:
        self.panel.slide_out_up()
        self._next_scene_factory = "play_again"

    def _go_to_main_menu(self) -> None:
        self.panel.slide_out_down()
        self._next_scene_factory = "main_menu"

    # ---------- update / render ----------

    def update(self) -> None:
        # World is frozen during game over — the crash freezes the scene; only the
        # panel animates in/out.
        self.panel.update(self.settings.window.height)

        if self.panel.is_done and self._next_scene_factory is not None:
            # In both branches the player car becomes a faux AI car so it sweeps
            # off-screen alongside the rest of the traffic during the transition.
            p = self.world.player
            if p is not None:
                fake_model = CarModel(p.image, p.rect.width, p.rect.height)
                fake = AICar(fake_model, p.rect.x, 0)
                fake.rect.y = p.rect.y
                self.world.ai_cars.add(fake)
                self.world.remove_player()
            from .transition import TransitionScene

            if self._next_scene_factory == "play_again":
                from .countdown import CountdownScene

                self.app.set_scene(TransitionScene, next_factory=CountdownScene)
            else:
                from .main_menu import MainMenuScene

                self.app.set_scene(TransitionScene, next_factory=MainMenuScene)

    def render(self, screen: pygame.Surface) -> None:
        self.world.render_background(screen)
        if not self.panel.is_done:
            self._render_panel(screen)
        icon = self.mute_icon if self.world.muted else self.unmute_icon
        screen.blit(icon, self.mute_icon_rect)

    def _render_panel(self, screen: pygame.Surface) -> None:
        self.panel.render(screen)
        cx, cy = self.panel.center_x, int(self.panel.center_y)
        theme = self.settings.theme
        accent = tuple(theme.text_accent)
        accent_button = tuple(theme.button_primary)

        # Leaderboard background + title + entries
        lb_rect = self._abs_rect(self.lb_offset, self.lb_size)
        screen.blit(self.lb_bg, lb_rect)
        title = self.lb_title_font.render("Leaderboard", True, accent_button)
        screen.blit(title, title.get_rect(center=(lb_rect.left + self.lb_size[0] // 2 - 20, lb_rect.top + 30)))
        screen.blit(self.reset_icon, self._abs_rect(self.reset_offset, self.reset_size))
        entry_y = lb_rect.top + 70
        for i, entry in enumerate(self.app.leaderboard.entries(), start=1):
            line = self._format_entry(i, entry.name, entry.score)
            label = self.lb_entry_font.render(line, True, accent_button)
            screen.blit(label, (lb_rect.left + 30, entry_y))
            entry_y += 45

        # Score box
        score_rect = self._abs_rect(self.score_offset, self.score_size)
        screen.blit(self.score_bg, score_rect)
        if self.rank is not None:
            current_entry = self.app.leaderboard.entries()[self.rank - 1]
            line = self._format_entry(self.rank, current_entry.name, current_entry.score)
            label = self.rank_score_font.render(line, True, accent_button)
            screen.blit(label, label.get_rect(center=(score_rect.centerx, score_rect.top + int(self.score_size[1] * 0.3))))
            hint = self.hint_font.render("Enter your name to display it", True, accent_button)
            screen.blit(hint, hint.get_rect(center=(score_rect.centerx, score_rect.top + int(self.score_size[1] * 0.7))))
            hint2 = self.hint_font.render("on the leaderboard!", True, accent_button)
            screen.blit(hint2, hint2.get_rect(center=(score_rect.centerx, score_rect.top + int(self.score_size[1] * 0.7) + 15)))
        else:
            score_label = self.score_big_font.render(str(self.score), True, accent_button)
            screen.blit(score_label, score_label.get_rect(center=score_rect.center))

        # Buttons
        screen.blit(self.pa_surface, self._abs_rect(self.pa_offset, self.pa_size))
        screen.blit(self.mm_surface, self._abs_rect(self.mm_offset, self.mm_size))

    @staticmethod
    def _format_entry(rank: int, name: str, score: int) -> str:
        return f"{rank}. {name:_<6} - {score}"
