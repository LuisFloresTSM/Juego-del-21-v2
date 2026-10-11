# Juego 21 (Game 21)

A complete, modular desktop application built in **Python 3** and **Pygame** adhering to strict Object-Oriented Programming (OOP) principles and formal AI Perception-Action agent modeling.

---

## 🎯 Game Objective & Rules

The objective is to obtain the combination **`(2, 1)` or `(1, 2)`** using two six-sided dice (faces 1 through 6) in the **minimum possible number of rolls/turns**.

### Performance Criterion
- Every roll action has a **cost of 1**.
- Minimizing the total number of rolls/turns to achieve the target combination is the performance measure.

### Environment & Sensors
- **Environment**: Two six-sided dice, each numbered 1 to 6.
- **Sensors / Observation**: 
  - Current numerical value of each die (`1-6` or `None`).
  - Fixed status of each die (`True` / `False`).
  - Total roll/turn count.
  - Game state: Initial, In Progress, Goal Reached.

### Restrictions Enforced
1. **Dice Values**: Generated with Python standard `random.randint(1, 6)`.
2. **Fixing Restriction**: A die can **only** be fixed when its current value is **1 or 2**.
3. **Irreversibility**: A die that has previously been fixed **cannot be unfixed** or rerolled.
4. **Immediate Victory**: When dice form `(2, 1)` or `(1, 2)`, the game terminates immediately.
5. **Accurate Cost Tracking**: The roll counter increments by 1 for each roll action (fixing does not count as a roll).

---

## 🤖 Perception → Action Rules

The intelligent agent implements the following formal rules:

| Condition / Perception | Recommended Action | Description |
| :--- | :--- | :--- |
| **Initial state** | `ROLL_BOTH` | Both dice are unfixed; roll both dice. |
| **Target pair `(2,1)` or `(1,2)`** | `DONE` | Goal reached immediately; game ends with victory. |
| **One die shows `1` or `2`** | `FIX_DIE` → `ROLL_OTHER` | Fix that die, then reroll only the remaining die. |
| **Both show same target `(1,1)` or `(2,2)`** | `FIX_DIE_1` → `ROLL_DIE_2` | Fix either die (Die 1 by convention), then reroll the other. |
| **Neither shows `1` nor `2`** | `ROLL_BOTH` | Reroll both dice. |

---

## 🧱 Software Architecture

Strict separation between **domain logic** and **presentation**:

```
juego21/
├── src/
│   ├── model/
│   │   ├── die.py          # Die class (value, fixed state, roll, validation)
│   │   ├── game.py         # Game21 class (rules, turns, actions, win condition, cost)
│   │   └── agent.py        # PerceptionActionAgent (formal Perception -> Action rules)
│   ├── ui/
│   │   ├── constants.py    # Colors, fonts, layouts, styling
│   │   ├── button.py       # Reusable button component with hover & tooltips
│   │   ├── die_view.py     # 3D dice rendering, authentic pips, fixed badges, roll animation
│   │   ├── particles.py    # Celebration confetti system on victory
│   │   └── app.py          # Pygame application loop, event handling, HUD
│   └── main.py             # Entry point (GUI + Monte Carlo policy simulation)
├── tests/
│   ├── test_game.py        # 22 unit tests covering all rules, constraints, edge cases
│   └── test_ui_headless.py # Headless Pygame integration test
├── run.bat                 # One-click Windows launcher
└── requirements.txt
```

---

## 🎮 How to Run

### 1. Launch the Desktop Pygame Application
In PowerShell or Command Prompt:
```powershell
cd C:\Users\lf201\.gemini\antigravity\scratch\juego21
.\.venv\Scripts\python.exe main.py
```
Or simply double-click `run.bat`.

### 2. Run Monte Carlo Policy Simulation
Simulate 10,000 games played automatically according to the Perception-Action rules:
```powershell
.\.venv\Scripts\python.exe main.py --simulate 10000
```

### 3. Run Test Suite
Verify all constraints, rules, and edge cases:
```powershell
.\.venv\Scripts\pytest.exe -v
```

---

## ⌨️ Controls & Shortcuts

| Action | Control Button | Keyboard Shortcut |
| :--- | :--- | :--- |
| **Roll Both Dice** | "Roll Both" | `[Space]` |
| **Roll Die 1** | "Roll Die 1" | `[1]` |
| **Roll Die 2** | "Roll Die 2" | `[2]` |
| **Fix Die 1 / 2** | "Fix Die 1 / 2" or Click Die directly | Click on Die face |
| **AI Advisor Step** | "AI Step" | `[A]` |
| **Auto-Play Mode** | "Auto-Play" / "Pause Auto" | `[P]` |
| **New Game / Reset**| "New Game" | `[R]` |
| **Exit** | Close Window | `[Esc]` |
