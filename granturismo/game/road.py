from __future__ import annotations

import pygame


class Road:
    """Centered scrolling road with N lanes, lane stripes, and red/white side stripes.

    All positions are computed from a single monotonic scroll counter; we never
    pop/append to a position list, which was the source of the O(n^2) churn
    in v1.
    """

    def __init__(self, settings):
        s = settings.road
        win = settings.window
        self.window_width = win.width
        self.window_height = win.height
        self.lane_width = s.lane_width
        self.lane_count = s.lane_count
        self.bg_color = tuple(s.background_color)
        self.lane_color = tuple(s.lane_color)
        self.lines_color = tuple(s.lines_color)
        self.lines_height = s.lines_height
        self.lines_width = s.lines_width
        self.lines_margin = s.lines_margin
        self.side_h = s.side_lines_height
        self.side_w = s.side_lines_width
        self.side_colors = [tuple(c) for c in s.side_lines_colors]

        road_pixel_width = self.lane_count * self.lane_width
        self.road_left = (self.window_width // 2) - (road_pixel_width // 2)
        self.road_right = self.road_left + road_pixel_width

        self._lane_line_xs = [
            self.road_left + (self.lane_width * i) - (self.lines_width // 2)
            for i in range(1, self.lane_count)
        ]

        self.scroll: float = 0.0

    def lane_x(self, lane: int, sprite_width: int) -> int:
        """1-based lane index → top-left x that centers a sprite in that lane."""
        center = self.road_left + (lane - 0.5) * self.lane_width
        return int(center - sprite_width / 2)

    def update(self, speed: float) -> None:
        self.scroll += speed

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(self.bg_color)
        pygame.draw.rect(
            screen,
            self.lane_color,
            (self.road_left, 0, self.lane_count * self.lane_width, self.window_height),
        )
        # Lane stripes (dashed white between lanes)
        period = self.lines_height + self.lines_margin
        shift = self.scroll % period
        y = -self.lines_height + shift
        while y < self.window_height:
            for x in self._lane_line_xs:
                pygame.draw.rect(
                    screen, self.lines_color, (x, int(y), self.lines_width, self.lines_height)
                )
            y += period
        # Side stripes (alternating red/white)
        pair = self.side_h * 2
        shift = self.scroll % pair
        y = -pair + shift
        cnt = 0
        c0, c1 = self.side_colors
        while y < self.window_height:
            color = c0 if cnt % 2 == 0 else c1
            pygame.draw.rect(
                screen, color, (self.road_left - self.side_w, int(y), self.side_w, self.side_h)
            )
            pygame.draw.rect(
                screen, color, (self.road_right, int(y), self.side_w, self.side_h)
            )
            y += self.side_h
            cnt += 1
