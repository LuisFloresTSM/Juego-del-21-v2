"""
Main entry point for Juego 21 (Game 21).

Usage:
    python main.py             # Launches the Pygame graphical interface
    python main.py --simulate  # Runs 10,000 automated policy simulations & reports metrics
"""
import sys
import os
import argparse

# Ensure current folder is in Python sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model.game import Game21
from src.model.agent import PerceptionActionAgent


def run_simulation(num_games: int = 10000) -> None:
    """Run Monte Carlo simulation of the Perception -> Action agent policy."""
    print(f"\n===========================================================")
    print(f"  Juego 21: Monte Carlo Policy Simulation ({num_games:,} games)")
    print(f"===========================================================")

    roll_counts = []
    distribution = {}

    for _ in range(num_games):
        game = Game21()
        rolls = PerceptionActionAgent.run_until_win(game)
        roll_counts.append(rolls)
        distribution[rolls] = distribution.get(rolls, 0) + 1

    avg_rolls = sum(roll_counts) / len(roll_counts)
    min_rolls = min(roll_counts)
    max_rolls = max(roll_counts)

    print(f"Performance Metrics (Minimizing Rolls/Turns):")
    print(f"  • Total games simulated:  {num_games:,}")
    print(f"  • Average rolls to win:    {avg_rolls:.3f}")
    print(f"  • Minimum rolls to win:    {min_rolls} (instant win on 1st roll)")
    print(f"  • Maximum rolls to win:    {max_rolls}")
    print("\nRoll Count Distribution:")
    for rolls in sorted(distribution.keys())[:10]:
        count = distribution[rolls]
        pct = (count / num_games) * 100
        bar = "#" * int(pct // 2)
        print(f"  {rolls:2d} rolls: {count:6d} ({pct:5.2f}%) {bar}")
    if len(distribution) > 10:
        remaining = sum(distribution[r] for r in sorted(distribution.keys())[10:])
        pct = (remaining / num_games) * 100
        print(f"  >10 rolls: {remaining:6d} ({pct:5.2f}%)")
    print(f"===========================================================\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Juego 21 (Game 21) — AI Dice Simulation & Player")
    parser.add_argument(
        "--simulate",
        nargs="?",
        const=10000,
        type=int,
        help="Run Monte Carlo simulation with N games (default: 10,000) and display statistics.",
    )

    args = parser.parse_args()

    if args.simulate is not None:
        run_simulation(args.simulate)
    else:
        # Launch Desktop Pygame GUI
        from src.ui.app import Game21App
        app = Game21App()
        app.run()


if __name__ == "__main__":
    main()
