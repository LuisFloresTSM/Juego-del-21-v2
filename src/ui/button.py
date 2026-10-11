"""
Interactive UI Button component for Pygame.
"""
import pygame
from typing import Callable, Optional, Tuple
from .constants import (
    COLOR_BTN_PRIMARY,
    COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_DISABLED,
    COLOR_BTN_TEXT_DISABLED,
    COLOR_TEXT_PRIMARY,
)


class Button:
    """A sleek clickable button with hover feedback, rounded borders, and tooltip."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        color_normal: Tuple[int, int, int] = COLOR_BTN_PRIMARY,
        color_hover: Tuple[int, int, int] = COLOR_BTN_PRIMARY_HOVER,
        color_disabled: Tuple[int, int, int] = COLOR_BTN_DISABLED,
        shortcut: Optional[str] = None,
        tooltip: Optional[str] = None,
        border_radius: int = 8,
    ):
        self.rect = rect
        self.text = text
        self.on_click = on_click
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_disabled = color_disabled
        self.shortcut = shortcut
        self.tooltip = tooltip
        self.border_radius = border_radius
        self.is_enabled: bool = True
        self.is_hovered: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process mouse motion and click events. Returns True if button was triggered."""
        if not self.is_enabled:
            self.is_hovered = False
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True

        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, small_font: Optional[pygame.font.Font] = None) -> None:
        """Render the button with state-appropriate colors and labels."""
        if not self.is_enabled:
            bg_color = self.color_disabled
            text_color = COLOR_BTN_TEXT_DISABLED
            border_color = (bg_color[0] + 10, bg_color[1] + 10, bg_color[2] + 10)
        elif self.is_hovered:
            bg_color = self.color_hover
            text_color = COLOR_TEXT_PRIMARY
            border_color = (255, 255, 255, 80)
        else:
            bg_color = self.color_normal
            text_color = COLOR_TEXT_PRIMARY
            border_color = (bg_color[0] - 15, bg_color[1] - 15, bg_color[2] - 15)

        # Draw main button body
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, border_color, self.rect, width=1, border_radius=self.border_radius)

        # Draw button label
        label_surf = font.render(self.text, True, text_color)
        label_rect = label_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (4 if self.shortcut else 0)))
        surface.blit(label_surf, label_rect)

        # Draw shortcut key hint if present
        if self.shortcut and small_font:
            hint_color = COLOR_BTN_TEXT_DISABLED if not self.is_enabled else (200, 210, 225)
            shortcut_surf = small_font.render(self.shortcut, True, hint_color)
            shortcut_rect = shortcut_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 10))
            surface.blit(shortcut_surf, shortcut_rect)
