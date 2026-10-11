"""
Game21 model managing game state, rules, actions, and goal detection.
"""
from typing import Dict, List, Optional, Tuple, Any
from .die import Die


class Game21:
    """
    Manages Juego 21 (Game 21).
    
    Objective:
        Obtain the target pair (2, 1) or (1, 2) in the minimum possible number of turns/rolls.
    
    Restrictions:
        - Two six-sided dice (1-6).
        - A die that has been fixed cannot be unfixed or rerolled.
        - A die may only be fixed when its current value is 1 or 2.
        - The game terminates immediately when the target combination (2,1) or (1,2) is achieved.
        - Every roll has a cost of 1; rolls are counted accurately.
    """

    TARGET_PAIRS = {(1, 2), (2, 1)}

    def __init__(self):
        self.die1 = Die(1)
        self.die2 = Die(2)
        self.roll_count: int = 0
        self.game_over: bool = False
        self.status_message: str = "Game started. Roll both dice to begin."
        self.last_action: Optional[str] = None
        self.history: List[Dict[str, Any]] = []

    @property
    def dice(self) -> Tuple[Die, Die]:
        return self.die1, self.die2

    def get_die(self, die_id: int) -> Die:
        if die_id == 1:
            return self.die1
        if die_id == 2:
            return self.die2
        raise ValueError(f"Invalid die id {die_id}. Must be 1 or 2.")

    def is_goal_reached(self) -> bool:
        """Check if current dice values form the winning combination (2,1) or (1,2)."""
        if self.die1.value is None or self.die2.value is None:
            return False
        return (self.die1.value, self.die2.value) in self.TARGET_PAIRS

    def can_roll_both(self) -> bool:
        """Both dice can be rolled if the game is active and neither die is fixed."""
        return (not self.game_over) and (not self.die1.is_fixed) and (not self.die2.is_fixed)

    def can_roll_die(self, die_id: int) -> bool:
        """A specific die can be rolled if the game is active and that die is not fixed."""
        if self.game_over:
            return False
        die = self.get_die(die_id)
        return die.can_roll()

    def can_fix_die(self, die_id: int) -> bool:
        """A specific die can be fixed if game is active and die satisfies fixing conditions."""
        if self.game_over:
            return False
        die = self.get_die(die_id)
        return die.can_fix()

    def roll_both(self, forced_values: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        """
        Roll both dice simultaneously.
        Increments the roll counter by 1.
        
        Args:
            forced_values: Optional tuple (v1, v2) for testing.
        """
        if self.game_over:
            raise ValueError("Game is already completed. Start a new game to roll again.")

        if not self.can_roll_both():
            raise ValueError("Cannot roll both dice when one or more dice are already fixed.")

        v1 = forced_values[0] if forced_values else None
        v2 = forced_values[1] if forced_values else None

        val1 = self.die1.roll(v1)
        val2 = self.die2.roll(v2)
        self.roll_count += 1
        self.last_action = f"Rolled both dice -> ({val1}, {val2})"

        self._evaluate_state_after_roll()
        self._record_history("ROLL_BOTH")
        return val1, val2

    def roll_die(self, die_id: int, forced_value: Optional[int] = None) -> int:
        """
        Roll only one individual die (allowed if that die is not fixed).
        Increments the roll counter by 1.
        
        Args:
            die_id: 1 or 2.
            forced_value: Optional value for testing.
        """
        if self.game_over:
            raise ValueError("Game is already completed. Start a new game to roll again.")

        die = self.get_die(die_id)
        if not die.can_roll():
            raise ValueError(f"Die {die_id} is fixed and cannot be rolled.")

        new_val = die.roll(forced_value)
        self.roll_count += 1
        self.last_action = f"Rolled Die {die_id} -> {new_val}"

        self._evaluate_state_after_roll()
        self._record_history(f"ROLL_DIE_{die_id}")
        return new_val

    def fix_die(self, die_id: int) -> None:
        """
        Fix an individual die.
        Die must not already be fixed, and its current value must be 1 or 2.
        Does not cost a roll.
        """
        if self.game_over:
            raise ValueError("Game is already completed.")

        die = self.get_die(die_id)
        die.fix()
        self.last_action = f"Fixed Die {die_id} (value={die.value})"

        # Check if fixing this die completes or clarifies the state
        if self.is_goal_reached():
            self.game_over = True
            self.status_message = (
                f"TARGET ACHIEVED ({self.die1.value}, {self.die2.value})! "
                f"Completed in {self.roll_count} roll{'s' if self.roll_count != 1 else ''}!"
            )
        else:
            other_id = 2 if die_id == 1 else 1
            other_die = self.get_die(other_id)
            if not other_die.is_fixed:
                self.status_message = f"Die {die_id} fixed ({die.value}). Reroll Die {other_id}."
            else:
                self.status_message = f"Die {die_id} fixed ({die.value})."

        self._record_history(f"FIX_DIE_{die_id}")

    def _evaluate_state_after_roll(self) -> None:
        """Check if the goal state is achieved or update status instructions."""
        if self.is_goal_reached():
            self.game_over = True
            self.status_message = (
                f"VICTORY! Target combination ({self.die1.value}, {self.die2.value}) achieved in "
                f"{self.roll_count} roll{'s' if self.roll_count != 1 else ''}!"
            )
            return

        v1 = self.die1.value
        v2 = self.die2.value
        f1 = self.die1.is_fixed
        f2 = self.die2.is_fixed

        if f1 and not f2:
            self.status_message = f"Die 1 is fixed at {v1}. Reroll Die 2."
        elif f2 and not f1:
            self.status_message = f"Die 2 is fixed at {v2}. Reroll Die 1."
        elif not f1 and not f2:
            if v1 in (1, 2) and v2 not in (1, 2):
                self.status_message = f"Die 1 shows useful value {v1}. Fix Die 1, then reroll Die 2."
            elif v2 in (1, 2) and v1 not in (1, 2):
                self.status_message = f"Die 2 shows useful value {v2}. Fix Die 2, then reroll Die 1."
            elif v1 in (1, 2) and v2 in (1, 2):
                self.status_message = f"Both dice show {v1}. Fix either die, then reroll the other."
            else:
                self.status_message = f"Neither die shows 1 or 2. Reroll both dice."

    def _record_history(self, action_name: str) -> None:
        """Record the state transition for auditing and analytics."""
        self.history.append({
            "action": action_name,
            "roll_count": self.roll_count,
            "die1_value": self.die1.value,
            "die1_fixed": self.die1.is_fixed,
            "die2_value": self.die2.value,
            "die2_fixed": self.die2.is_fixed,
            "game_over": self.game_over,
            "status": self.status_message,
        })

    def get_state(self) -> Dict[str, Any]:
        """Return the complete logical state observation."""
        return {
            "die1_value": self.die1.value,
            "die1_fixed": self.die1.is_fixed,
            "die2_value": self.die2.value,
            "die2_fixed": self.die2.is_fixed,
            "roll_count": self.roll_count,
            "game_over": self.game_over,
            "goal_reached": self.is_goal_reached(),
            "status_message": self.status_message,
            "last_action": self.last_action,
        }

    def get_available_actions(self) -> List[str]:
        """Return list of valid actions currently possible."""
        if self.game_over:
            return []

        actions = []
        if self.can_roll_both():
            actions.append("ROLL_BOTH")
        if self.can_roll_die(1) and (self.die2.is_fixed or self.die1.value is not None):
            actions.append("ROLL_DIE_1")
        if self.can_roll_die(2) and (self.die1.is_fixed or self.die2.value is not None):
            actions.append("ROLL_DIE_2")
        if self.can_fix_die(1):
            actions.append("FIX_DIE_1")
        if self.can_fix_die(2):
            actions.append("FIX_DIE_2")
        return actions

    def reset(self) -> None:
        """Reset the game back to the initial unrolled state."""
        self.die1.reset()
        self.die2.reset()
        self.roll_count = 0
        self.game_over = False
        self.status_message = "Game reset. Roll both dice to begin."
        self.last_action = None
        self.history.clear()
