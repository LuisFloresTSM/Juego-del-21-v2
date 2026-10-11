"""
UI constants, color palettes, and layout configuration for Juego 21.
"""
import pygame

# Window configuration
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Juego 21 (Game 21) — AI Dice Simulation & Player"

# Color Palette (Modern Dark / Slate Theme)
COLOR_BG = (18, 22, 34)              # Deep navy dark background
COLOR_PANEL = (28, 34, 52)           # Card/panel container
COLOR_PANEL_BORDER = (46, 56, 84)    # Panel border
COLOR_HEADER = (15, 18, 28)          # Top bar

# Text colors
COLOR_TEXT_PRIMARY = (245, 247, 250)
COLOR_TEXT_MUTED = (145, 158, 178)
COLOR_TEXT_ACCENT = (74, 144, 226)

# State Colors
COLOR_SUCCESS = (46, 204, 113)       # Green / Victory
COLOR_SUCCESS_BG = (24, 76, 48)
COLOR_WARNING = (241, 196, 15)       # Amber / Fix target
COLOR_DANGER = (231, 76, 60)         # Red
COLOR_INFO = (52, 152, 219)          # Blue info

# Die visual styling
COLOR_DIE_UNFIXED_BG = (245, 246, 250)
COLOR_DIE_UNFIXED_BORDER = (189, 195, 199)
COLOR_DIE_FIXED_BG = (255, 248, 220)
COLOR_DIE_FIXED_BORDER = (241, 196, 15)       # Gold
COLOR_DIE_FIXED_GLOW = (255, 215, 0, 70)
COLOR_DIE_PIP_STANDARD = (33, 37, 41)
COLOR_DIE_PIP_TARGET = (220, 53, 69)          # Red pips for target values 1 and 2

# Button styling
COLOR_BTN_PRIMARY = (52, 152, 219)
COLOR_BTN_PRIMARY_HOVER = (41, 128, 185)
COLOR_BTN_SUCCESS = (46, 204, 113)
COLOR_BTN_SUCCESS_HOVER = (39, 174, 96)
COLOR_BTN_WARNING = (243, 156, 18)
COLOR_BTN_WARNING_HOVER = (211, 84, 0)
COLOR_BTN_SECONDARY = (50, 60, 85)
COLOR_BTN_SECONDARY_HOVER = (65, 78, 110)
COLOR_BTN_DISABLED = (38, 44, 62)
COLOR_BTN_TEXT_DISABLED = (90, 100, 120)
