"""
Visual rendering and animation component for a Die in Juego 21.
"""
import random
import pygame
from typing import Optional, Tuple
from ..model.die import Die
from .constants import (
    COLOR_DIE_UNFIXED_BG,
    COLOR_DIE_UNFIXED_BORDER,
    COLOR_DIE_FIXED_BG,
    COLOR_DIE_FIXED_BORDER,
    COLOR_DIE_PIP_STANDARD,
    COLOR_DIE_PIP_TARGET,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
)


class DieView:
    """Renders an individual die with authentic pips, fixed badges, and roll animations."""

    def __init__(self, die: Die, center_x: int, center_y: int, size: int = 150):
        self.die = die
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.rect = pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)

        # Animation states
        self.is_animating: bool = False
        self.animation_timer: int = 0
        self.animation_duration: int = 350  # milliseconds
        self.displayed_fake_value: int = 1
        self.shake_offset: Tuple[int, int] = (0, 0)
        self.is_hovered: bool = False

    def start_roll_animation(self, duration_ms: int = 350) -> None:
        """Trigger visual roll tumble if the die is not fixed."""
        if self.die.is_fixed:
            return
        self.is_animating = True
        self.animation_timer = pygame.time.get_ticks()
        self.animation_duration = duration_ms

    def update(self) -> None:
        """Update animation frames and tumbling pips."""
        if not self.is_animating:
            self.shake_offset = (0, 0)
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.animation_timer

        if elapsed >= self.animation_duration:
            self.is_animating = False
            self.shake_offset = (0, 0)
        else:
            # Shake and cycle random face numbers
            self.displayed_fake_value = random.randint(1, 6)
            self.shake_offset = (random.randint(-3, 3), random.randint(-3, 3))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse hover and click events. Returns True if clicked to fix."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.die.can_fix():
                return True

        return False

    def draw(
        self,
        surface: pygame.Surface,
        font_large: pygame.font.Font,
        font_small: pygame.font.Font,
        font_badge: pygame.font.Font,
    ) -> None:
        """Draw the complete die card, face, pips, and state annotations."""
        ox, oy = self.shake_offset
        draw_rect = self.rect.move(ox, oy)

        # Determine visual style based on fixed / unfixed state
        if self.die.is_fixed:
            bg_color = COLOR_DIE_FIXED_BG
            border_color = COLOR_DIE_FIXED_BORDER
            border_width = 4
        else:
            bg_color = COLOR_DIE_UNFIXED_BG
            border_color = (120, 180, 250) if (self.is_hovered and self.die.can_fix()) else COLOR_DIE_UNFIXED_BORDER
            border_width = 3 if (self.is_hovered and self.die.can_fix()) else 2

        # Draw drop shadow
        shadow_rect = draw_rect.move(4, 6)
        pygame.draw.rect(surface, (10, 12, 18, 120), shadow_rect, border_radius=18)

        # Draw die body
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=18)
        pygame.draw.rect(surface, border_color, draw_rect, width=border_width, border_radius=18)

        # Determine value to display
        if self.is_animating:
            value_to_draw = self.displayed_fake_value
        else:
            value_to_draw = self.die.value

        # Draw pips or placeholder question mark
        if value_to_draw is None:
            # Unrolled die
            q_surf = font_large.render("?", True, COLOR_TEXT_MUTED)
            q_rect = q_surf.get_rect(center=draw_rect.center)
            surface.blit(q_surf, q_rect)
        else:
            # Render authentic die pips
            self._draw_pips(surface, draw_rect, value_to_draw)

        # Top label: "DIE 1" or "DIE 2"
        die_title = f"DIE {self.die.id}"
        title_surf = font_small.render(die_title, True, COLOR_TEXT_PRIMARY)
        title_rect = title_surf.get_rect(center=(self.center_x, self.rect.top - 20))
        surface.blit(title_surf, title_rect)

        # Bottom badge: Fixed or Unfixed status
        self._draw_status_badge(surface, font_badge)

    def _draw_status_badge(self, surface: pygame.Surface, font_badge: pygame.font.Font) -> None:
        """Render the status pill below the die."""
        badge_y = self.rect.bottom + 16
        if self.die.is_fixed:
            text = f"LOCKED (Fixed: {self.die.value})"
            badge_bg = (180, 140, 20)
            badge_border = COLOR_WARNING
            text_color = (255, 255, 255)
        elif self.die.can_fix():
            if self.is_hovered:
                text = "CLICK TO FIX 🔒"
                badge_bg = (39, 174, 96)
                badge_border = COLOR_SUCCESS
            else:
                text = f"TARGET VALUE {self.die.value} (CAN FIX)"
                badge_bg = (41, 128, 185)
                badge_border = (100, 180, 255)
            text_color = (255, 255, 255)
        elif self.die.value is not None:
            text = f"Unfixed (Value: {self.die.value})"
            badge_bg = (40, 48, 68)
            badge_border = (65, 78, 105)
            text_color = (180, 190, 210)
        else:
            text = "Unrolled"
            badge_bg = (35, 42, 60)
            badge_border = (55, 65, 88)
            text_color = COLOR_TEXT_MUTED

        text_surf = font_badge.render(text, True, text_color)
        badge_rect = pygame.Rect(0, 0, text_surf.get_width() + 18, 24)
        badge_rect.center = (self.center_x, badge_y)

        pygame.draw.rect(surface, badge_bg, badge_rect, border_radius=12)
        pygame.draw.rect(surface, badge_border, badge_rect, width=1, border_radius=12)
        surface.blit(text_surf, text_surf.get_rect(center=badge_rect.center))

    def _draw_pips(self, surface: pygame.Surface, rect: pygame.Rect, value: int) -> None:
        """Render the pips on the die face based on integer value 1 to 6."""
        # Target values 1 and 2 get vibrant highlighted pips
        pip_color = COLOR_DIE_PIP_TARGET if (value in (1, 2) and not self.is_animating) else COLOR_DIE_PIP_STANDARD

        pip_radius = int(self.size * 0.082)
        cx, cy = rect.center
        offset = int(self.size * 0.26)

        # Pip coordinate mapping
        top_left = (cx - offset, cy - offset)
        top_right = (cx + offset, cy - offset)
        mid_left = (cx - offset, cy)
        center = (cx, cy)
        mid_right = (cx + offset, cy)
        bot_left = (cx - offset, cy + offset)
        bot_right = (cx + offset, cy + offset)

        positions = []
        if value == 1:
            positions = [center]
        elif value == 2:
            positions = [top_left, bot_right]
        elif value == 3:
            positions = [top_left, center, bot_right]
        elif value == 4:
            positions = [top_left, top_right, bot_left, bot_right]
        elif value == 5:
            positions = [top_left, top_right, center, bot_left, bot_right]
        elif value == 6:
            positions = [top_left, top_right, mid_left, mid_right, bot_left, bot_right]

        for pos in positions:
            # Pip outer bevel/shadow for 3D realism
            pygame.draw.circle(surface, (200, 200, 200), (pos[0], pos[1] + 1), pip_radius)
            # Main pip
            pygame.draw.circle(surface, pip_color, pos, pip_radius)
            # Subtle specular shine
            pygame.draw.circle(surface, (255, 255, 255, 120), (pos[0] - 2, pos[1] - 2), max(1, pip_radius // 3))
