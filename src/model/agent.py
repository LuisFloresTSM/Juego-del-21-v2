"""
Intelligent Agent implementing the Perception -> Action rules for Juego 21.
"""
from typing import Tuple, Optional
from .game import Game21


class PerceptionActionAgent:
    """
    An agent that implements the formal Perception -> Action rules:
    
    1. Initial State:
       Both dice are unfixed -> Roll both dice.
    2. Both dice form target pair (2,1) or (1,2):
       Game ends immediately (Victory).
    3. One die shows a target value (1 or 2):
       Fix that die, then reroll only the other die.
    4. Both dice show the same target value (1,1 or 2,2):
       Fix either die (convention: Die 1), then reroll the other die.
    5. Neither die shows a target value:
       Reroll both dice.
    """

    @staticmethod
    def decide_action(game: Game21) -> Tuple[str, str]:
        """
        Analyze current game state (Perception) and determine the next action (Action).
        
        Returns:
            Tuple of (action_type, explanation_string)
            action_type is one of:
            - "DONE": Target reached or game finished
            - "ROLL_BOTH": Roll both dice
            - "ROLL_DIE_1": Reroll Die 1
            - "ROLL_DIE_2": Reroll Die 2
            - "FIX_DIE_1": Fix Die 1
            - "FIX_DIE_2": Fix Die 2
        """
        if game.game_over or game.is_goal_reached():
            return "DONE", "Target combination (2,1) or (1,2) achieved! Game finished."

        d1 = game.die1
        d2 = game.die2

        # Initial state: dice not yet rolled
        if d1.value is None or d2.value is None:
            return "ROLL_BOTH", "Initial state: Roll both dice."

        # Case: Die 1 is already fixed
        if d1.is_fixed and not d2.is_fixed:
            return "ROLL_DIE_2", f"Die 1 is fixed at {d1.value}. Reroll only Die 2."

        # Case: Die 2 is already fixed
        if d2.is_fixed and not d1.is_fixed:
            return "ROLL_DIE_1", f"Die 2 is fixed at {d2.value}. Reroll only Die 1."

        # Case: Neither die is fixed
        v1 = d1.value
        v2 = d2.value

        # Target pair reached (already checked above, but safe guard)
        if (v1, v2) in Game21.TARGET_PAIRS:
            return "DONE", f"Both dice form the target pair ({v1}, {v2})! Game ends immediately."

        # Both dice show the same target value (1,1 or 2,2)
        if v1 in (1, 2) and v2 in (1, 2) and v1 == v2:
            return "FIX_DIE_1", f"Both dice show same target value ({v1},{v2}). Fix Die 1 and reroll Die 2."

        # Die 1 shows a target value (1 or 2)
        if v1 in (1, 2) and v2 not in (1, 2):
            return "FIX_DIE_1", f"Die 1 shows target value {v1}. Fix Die 1, then reroll Die 2."

        # Die 2 shows a target value (1 or 2)
        if v2 in (1, 2) and v1 not in (1, 2):
            return "FIX_DIE_2", f"Die 2 shows target value {v2}. Fix Die 2, then reroll Die 1."

        # Neither die shows a target value
        return "ROLL_BOTH", f"Neither die shows 1 or 2 ({v1}, {v2}). Reroll both dice."

    @classmethod
    def step(cls, game: Game21) -> Tuple[str, str]:
        """
        Execute one perception-action step on the game.
        
        Returns:
            Tuple of (action_executed, description)
        """
        action, reason = cls.decide_action(game)

        if action == "ROLL_BOTH":
            game.roll_both()
        elif action == "ROLL_DIE_1":
            game.roll_die(1)
        elif action == "ROLL_DIE_2":
            game.roll_die(2)
        elif action == "FIX_DIE_1":
            game.fix_die(1)
        elif action == "FIX_DIE_2":
            game.fix_die(2)
        elif action == "DONE":
            pass

        return action, reason

    @classmethod
    def run_until_win(cls, game: Game21, max_steps: int = 200) -> int:
        """
        Run the agent automatically until the target state is reached.
        
        Returns:
            Total rolls/turns taken to win.
        """
        steps = 0
        while not game.game_over and steps < max_steps:
            cls.step(game)
            steps += 1
        return game.roll_count
