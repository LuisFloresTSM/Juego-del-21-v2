"""
Unit tests validating all rules, constraints, and behaviors for Juego 21.
"""
import pytest
from src.model.die import Die
from src.model.game import Game21
from src.model.agent import PerceptionActionAgent


class TestDie:
    """Tests for the Die model."""

    def test_die_initial_state(self):
        die = Die(1)
        assert die.id == 1
        assert die.value is None
        assert not die.is_fixed
        assert die.can_roll()
        assert not die.can_fix()

    def test_die_invalid_id(self):
        with pytest.raises(ValueError):
            Die(3)

    def test_die_roll_produces_values_between_1_and_6(self):
        die = Die(1)
        for _ in range(100):
            val = die.roll()
            assert 1 <= val <= 6
            assert die.value == val

    def test_die_fix_only_on_target_values(self):
        die = Die(1)
        # Attempt fixing invalid values (3, 4, 5, 6)
        for val in (3, 4, 5, 6):
            die.roll(forced_value=val)
            assert not die.can_fix()
            with pytest.raises(ValueError, match="A die may only be fixed when its current value is 1 or 2"):
                die.fix()
            assert not die.is_fixed

        # Fixing valid target values 1 and 2
        for val in (1, 2):
            die.reset()
            die.roll(forced_value=val)
            assert die.can_fix()
            die.fix()
            assert die.is_fixed

    def test_fixed_die_cannot_be_rerolled(self):
        die = Die(1)
        die.roll(forced_value=2)
        die.fix()
        assert not die.can_roll()
        with pytest.raises(ValueError, match="is fixed and cannot be rerolled"):
            die.roll()

    def test_fixed_die_cannot_be_refixed_or_unfixed(self):
        die = Die(1)
        die.roll(forced_value=1)
        die.fix()
        assert die.is_fixed
        assert not die.can_fix()
        with pytest.raises(ValueError, match="already fixed"):
            die.fix()


class TestGame21:
    """Tests for Game21 mechanics and restrictions."""

    def test_game_initial_state(self):
        game = Game21()
        assert game.roll_count == 0
        assert not game.game_over
        assert game.die1.value is None
        assert game.die2.value is None
        assert game.can_roll_both()
        assert not game.is_goal_reached()

    def test_initial_roll_both(self):
        game = Game21()
        v1, v2 = game.roll_both(forced_values=(3, 5))
        assert game.roll_count == 1
        assert 1 <= v1 <= 6
        assert 1 <= v2 <= 6
        assert not game.game_over

    def test_target_pair_2_1_wins_immediately(self):
        game = Game21()
        game.roll_both(forced_values=(2, 1))
        assert game.roll_count == 1
        assert game.is_goal_reached()
        assert game.game_over

    def test_target_pair_1_2_wins_immediately(self):
        game = Game21()
        game.roll_both(forced_values=(1, 2))
        assert game.roll_count == 1
        assert game.is_goal_reached()
        assert game.game_over

    def test_fixing_die_and_rerolling_other_die(self):
        game = Game21()
        # Roll 1: die 1 gets 2, die 2 gets 5
        game.roll_both(forced_values=(2, 5))
        assert game.roll_count == 1
        assert not game.game_over

        # Fix die 1 (value 2)
        assert game.can_fix_die(1)
        assert not game.can_fix_die(2)
        game.fix_die(1)
        assert game.die1.is_fixed
        assert not game.die2.is_fixed
        assert game.roll_count == 1  # Fixing does NOT cost a roll

        # Cannot roll both anymore because die 1 is fixed
        assert not game.can_roll_both()
        with pytest.raises(ValueError, match="Cannot roll both dice"):
            game.roll_both()

        # Cannot reroll die 1
        with pytest.raises(ValueError, match="Die 1 is fixed"):
            game.roll_die(1)

        # Roll die 2 until it hits 1
        game.roll_die(2, forced_value=4)
        assert game.roll_count == 2
        assert not game.game_over

        game.roll_die(2, forced_value=1)
        assert game.roll_count == 3
        assert game.is_goal_reached()
        assert game.game_over

    def test_both_dice_same_target_value_fix_one_reroll_other(self):
        # Both dice roll 2
        game = Game21()
        game.roll_both(forced_values=(2, 2))
        assert not game.game_over
        assert game.can_fix_die(1)
        assert game.can_fix_die(2)

        # Player chooses to fix die 2
        game.fix_die(2)
        assert game.die2.is_fixed
        assert not game.die1.is_fixed

        # Reroll die 1
        game.roll_die(1, forced_value=1)
        assert game.roll_count == 2
        assert game.is_goal_reached()
        assert game.game_over

    def test_neither_shows_target_value_reroll_both(self):
        game = Game21()
        game.roll_both(forced_values=(3, 6))
        assert not game.can_fix_die(1)
        assert not game.can_fix_die(2)
        assert game.can_roll_both()

        # Reroll both
        game.roll_both(forced_values=(4, 5))
        assert game.roll_count == 2
        assert not game.game_over

    def test_cannot_roll_after_game_over(self):
        game = Game21()
        game.roll_both(forced_values=(2, 1))
        assert game.game_over

        with pytest.raises(ValueError, match="Game is already completed"):
            game.roll_both()

        with pytest.raises(ValueError, match="Game is already completed"):
            game.roll_die(1)

    def test_reset_functionality(self):
        game = Game21()
        game.roll_both(forced_values=(2, 1))
        assert game.game_over
        game.reset()
        assert game.roll_count == 0
        assert not game.game_over
        assert game.die1.value is None
        assert game.die2.value is None
        assert not game.die1.is_fixed
        assert not game.die2.is_fixed


class TestPerceptionActionAgent:
    """Tests validating the Perception -> Action decision rules."""

    def test_initial_state_action(self):
        game = Game21()
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "ROLL_BOTH"

    def test_immediate_win_action(self):
        game = Game21()
        game.roll_both(forced_values=(1, 2))
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "DONE"

    def test_one_target_die1(self):
        game = Game21()
        game.roll_both(forced_values=(2, 4))
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "FIX_DIE_1"

        PerceptionActionAgent.step(game)
        assert game.die1.is_fixed

        next_action, _ = PerceptionActionAgent.decide_action(game)
        assert next_action == "ROLL_DIE_2"

    def test_one_target_die2(self):
        game = Game21()
        game.roll_both(forced_values=(5, 1))
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "FIX_DIE_2"

        PerceptionActionAgent.step(game)
        assert game.die2.is_fixed

        next_action, _ = PerceptionActionAgent.decide_action(game)
        assert next_action == "ROLL_DIE_1"

    def test_same_target_value(self):
        game = Game21()
        game.roll_both(forced_values=(1, 1))
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "FIX_DIE_1"

    def test_neither_target_value(self):
        game = Game21()
        game.roll_both(forced_values=(3, 5))
        action, _ = PerceptionActionAgent.decide_action(game)
        assert action == "ROLL_BOTH"

    def test_agent_run_until_win(self):
        game = Game21()
        turns = PerceptionActionAgent.run_until_win(game)
        assert turns >= 1
        assert game.game_over
        assert game.is_goal_reached()
        assert {game.die1.value, game.die2.value} == {1, 2}
