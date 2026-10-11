"""
Particle system for victory celebrations in Juego 21.
"""
import random
import pygame
from typing import List


class Particle:
    """Represents a single confetti particle."""

    COLORS = [
        (241, 196, 15),   # Gold
        (46, 204, 113),   # Emerald
        (52, 152, 219),   # Blue
        (231, 76, 60),    # Red
        (155, 89, 182),   # Purple
        (255, 121, 198),  # Pink
        (255, 255, 255),  # White
    ]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6.0, 6.0)
        self.vy = random.uniform(-10.0, -2.0)
        self.gravity = random.uniform(0.18, 0.32)
        self.size = random.uniform(5.0, 10.0)
        self.color = random.choice(self.COLORS)
        self.alpha = 255
        self.fade_rate = random.uniform(1.5, 3.5)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)

    def update(self) -> bool:
        """Update position and physics. Returns False when particle expires."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.rotation += self.rotation_speed
        self.alpha = max(0, self.alpha - self.fade_rate)
        return self.alpha > 0 and self.y < 800

    def draw(self, surface: pygame.Surface) -> None:
        """Render particle with transparency."""
        if self.alpha <= 0:
            return
        surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        color = (*self.color, int(self.alpha))
        pygame.draw.rect(
            surf,
            color,
            (int(self.size * 0.5), int(self.size * 0.5), int(self.size), int(self.size * 0.6))
        )
        rotated = pygame.transform.rotate(surf, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)


class ParticleSystem:
    """Manages emission and updating of particles."""

    def __init__(self):
        self.particles: List[Particle] = []
        self.active: bool = False

    def burst(self, x: float, y: float, count: int = 70) -> None:
        self.active = True
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def update(self) -> None:
        if not self.particles:
            self.active = False
            return
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)

    def clear(self) -> None:
        self.particles.clear()
        self.active = False
