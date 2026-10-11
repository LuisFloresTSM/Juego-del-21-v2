"""
Die model representing a single six-sided die.
"""
import random
from typing import Optional


class Die:
    """Represents an individual six-sided die with values 1 to 6 and a fixed state."""

    VALID_VALUES = (1, 2, 3, 4, 5, 6)
    TARGET_VALUES = (1, 2)

    def __init__(self, die_id: int):
        if die_id not in (1, 2):
            raise ValueError(f"Die ID must be 1 or 2, got {die_id}")
        self.id = die_id
        self._value: Optional[int] = None
        self._is_fixed: bool = False

    @property
    def value(self) -> Optional[int]:
        """Current numerical value shown by the die (1-6) or None if unrolled."""
        return self._value

    @property
    def is_fixed(self) -> bool:
        """Whether the die is fixed in place."""
        return self._is_fixed

    def can_roll(self) -> bool:
        """A die can be rolled if and only if it is not currently fixed."""
        return not self._is_fixed

    def can_fix(self) -> bool:
        """
        A die can be fixed if:
        1. It is not already fixed (cannot be fixed twice, cannot be unfixed).
        2. Its current value is a target value (1 or 2).
        """
        return (not self._is_fixed) and (self._value in self.TARGET_VALUES)

    def roll(self, forced_value: Optional[int] = None) -> int:
        """
        Roll the die to produce an integer value from 1 to 6.
        A fixed die cannot be rolled.
        
        Args:
            forced_value: Optional value for deterministic testing (must be 1-6).
        """
        if self._is_fixed:
            raise ValueError(f"Die {self.id} is fixed and cannot be rerolled.")

        if forced_value is not None:
            if forced_value not in self.VALID_VALUES:
                raise ValueError(f"Invalid die value {forced_value}. Must be between 1 and 6.")
            self._value = forced_value
        else:
            self._value = random.randint(1, 6)

        return self._value

    def fix(self) -> None:
        """
        Fix the die in place.
        Restrictions:
        - A die that has previously been fixed cannot be unfixed or re-fixed.
        - A die can only be fixed when its current value is 1 or 2.
        """
        if self._is_fixed:
            raise ValueError(f"Die {self.id} is already fixed. A fixed die cannot be modified.")

        if self._value not in self.TARGET_VALUES:
            raise ValueError(
                f"Die {self.id} cannot be fixed with value {self._value}. "
                f"A die may only be fixed when its current value is 1 or 2."
            )

        self._is_fixed = True

    def reset(self) -> None:
        """Reset the die to its initial unrolled and unfixed state."""
        self._value = None
        self._is_fixed = False

    def __repr__(self) -> str:
        return f"Die(id={self.id}, value={self._value}, fixed={self._is_fixed})"
