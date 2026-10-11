"""
Headless GUI integration test for Juego 21 Pygame UI.
"""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from src.ui.app import Game21App


def test_pygame_ui_lifecycle():
    """Verify Pygame initialization, frame rendering, event dispatching, and action execution."""
    app = Game21App()
    assert app.screen is not None

    # Frame 1: Initial state
    app.handle_events()
    app.update()
    app.draw()

    # Trigger action: Roll both dice
    app.action_roll_both()
    assert app.game.roll_count == 1
    app.update()
    app.draw()

    # Trigger action: Agent Step
    app.action_agent_step()
    app.update()
    app.draw()

    # Test New Game reset
    app.action_new_game()
    assert app.game.roll_count == 0
    app.update()
    app.draw()

    # Clean shutdown
    pygame.quit()
