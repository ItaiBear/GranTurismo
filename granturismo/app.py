from __future__ import annotations

import pygame

from .assets import AssetManager
from .config import Settings
from .game.leaderboard import Leaderboard
from .scenes.base import Scene
from .world import World


class App:
    """Top-level scene manager, clock, event pump."""

    def __init__(self, settings_path: str = "config.json"):
        pygame.init()
        pygame.mixer.init()

        self.settings = Settings.load(settings_path)
        win = self.settings.window
        flags = pygame.FULLSCREEN if win.fullscreen else 0
        self.screen = pygame.display.set_mode((win.width, win.height), flags)
        pygame.display.set_caption(win.title)

        self.clock = pygame.time.Clock()
        self.assets = AssetManager(".")
        self.world = World(self.settings, self.assets)
        self.leaderboard = Leaderboard(
            self.settings.leaderboard.file,
            self.settings.leaderboard.size,
            self.settings.leaderboard.name_max_length,
        )

        # Start music
        self.assets.play_music(
            self.settings.audio.music_file, self.settings.audio.default_volume
        )
        if self.settings.audio.start_muted:
            pygame.mixer.music.set_volume(0)

        self.running = True
        self.scene: Scene
        from .scenes.main_menu import MainMenuScene

        self.set_scene(MainMenuScene)

    def set_scene(self, factory, **kwargs) -> None:
        self.scene = factory(self, **kwargs)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.scene.handle_event(event)
            if not self.running:
                break
            self.scene.update()
            self.scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(self.settings.window.fps)
        pygame.quit()
