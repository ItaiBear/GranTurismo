from __future__ import annotations

import pygame

from .assets import AssetManager
from .game.entities import AICar, CarModel, Player, Scenery
from .game.road import Road
from .game.spawner import try_spawn_ai, try_spawn_tree


class World:
    """Persistent scrolling world shared across scenes.

    Holds the road, the current scroll speed, scenery sprites, AI cars, and
    (when present) the player. Scenes mutate this state directly rather than
    each managing their own copies.
    """

    def __init__(self, settings, assets: AssetManager):
        self.settings = settings
        self.assets = assets

        self.road = Road(settings)
        self.speed: float = settings.player.speed
        self.cars_scroll_speed: int = settings.ai_cars.scroll_speed

        # Sprite groups
        self.trees = pygame.sprite.Group()
        self.ai_cars = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()

        # Models
        self.ai_models = [
            CarModel(
                assets.surface(c.file, transparent=tuple(c.transparent)),
                c.w,
                c.h,
            )
            for c in settings.ai_cars.sprites
        ]
        self.player_model = CarModel(
            assets.surface(settings.player.sprite, transparent=tuple(settings.player.transparent_color)),
            settings.player.width,
            settings.player.height,
        )
        self.tree_image = assets.surface(
            settings.scenery.tree_sprite, transparent=tuple(settings.scenery.tree_transparent)
        )

        self.muted: bool = settings.audio.start_muted
        self.volume: float = settings.audio.default_volume

    # ------- spawning + scrolling -------

    def spawn_step(self, density_scale: float = 1.0, include_cars: bool = True) -> None:
        s = self.settings
        try_spawn_tree(
            self.road,
            self.tree_image,
            s.scenery.tree_width,
            s.scenery.tree_height,
            max(1, int(s.scenery.tree_density / density_scale)),
            s.scenery.margin_from_road,
            self.trees,
        )
        if include_cars:
            car = try_spawn_ai(
                self.road,
                self.ai_cars,
                self.ai_models,
                s.ai_cars.base_density,
                self.player_model.height,
                s.ai_cars.spawn_margin,
                self.cars_scroll_speed,
            )
            if car is not None:
                self.ai_cars.add(car)

    def scroll_step(self) -> None:
        self.road.update(self.speed)
        self.trees.update(self.speed, self.road.window_height)
        self.ai_cars.update(self.speed, self.road.window_height)

    # ------- player lifecycle -------

    def reset_player(self, start_y: int, lane: int) -> Player:
        player = Player(
            self.player_model,
            self.road,
            lane,
            self.settings.player.horizontal_speed,
        )
        player.rect.y = start_y
        self.player_group.add(player)
        return player

    @property
    def player(self) -> Player | None:
        return self.player_group.sprite

    def remove_player(self) -> None:
        self.player_group.empty()

    # ------- volume / mute -------

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        if not self.muted:
            pygame.mixer.music.set_volume(self.volume)

    def toggle_mute(self) -> None:
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else self.volume)

    # ------- rendering -------

    def render_world(self, screen: pygame.Surface) -> None:
        """Road + scenery + AI cars. Does not draw the player — that's a separate
        layer so scenes can insert overlays (like the GO sign) between them.
        """
        self.road.render(screen)
        self.trees.draw(screen)
        self.ai_cars.draw(screen)

    def render_player(self, screen: pygame.Surface) -> None:
        self.player_group.draw(screen)

    def render_background(self, screen: pygame.Surface) -> None:
        """Full back-to-front world render including the player on top."""
        self.render_world(screen)
        self.render_player(screen)
