"""Visual constants for the QLEX terminal UI. Nothing hardcoded elsewhere."""

import curses

# Color pair IDs
PAIR_TITLE = 1
PAIR_ACCENT = 2
PAIR_DIM = 3
PAIR_BODY = 4
PAIR_SUCCESS = 5
PAIR_WARN = 6
PAIR_QOREX = 7

# Box-drawing glyph sets
GLYPHS_HEAVY = {
    "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
    "h": "━", "v": "┃",
    "lt": "┣", "rt": "┫", "tt": "┳", "bt": "┻", "cross": "╋",
}

GLYPHS_LIGHT = {
    "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
    "h": "─", "v": "│",
    "lt": "├", "rt": "┤", "tt": "┬", "bt": "┴", "cross": "┼",
}

# Animation constants
ANIM_FPS = 24
ANIM_TRANSITION_FRAMES = 8
CHAR_DENSITY = "█▓▒░ "

# QLEX ASCII Logo
LOGO = [
    " ████████  ██        ████████  ██    ██",
    " ██    ██  ██        ██         ██  ██ ",
    " ██    ██  ██        ████████    ████  ",
    " ██    ██  ██        ██         ██  ██ ",
    " ████████  ████████  ████████  ██    ██",
    "    ████                               ",
]

LOGO_SMALL = " QLEX "

BRAND = "by Qorex"

# Sitting cat tail-wag frames (8 chars wide, 4 rows tall)
CAT_FRAMES = [
    # Frame 0: tail left
    ["\\    /\\ ", " )  ( ')", "(  /  ) ", " \\(__)| "],
    # Frame 1: tail up
    [" |   /\\ ", " )  ( ')", "(  /  ) ", " \\(__)| "],
    # Frame 2: tail right
    ["  /  /\\ ", " )  ( ')", "(  /  ) ", " \\(__)| "],
    # Frame 3: tail up (pendulum back)
    [" |   /\\ ", " )  ( ')", "(  /  ) ", " \\(__)| "],
]
CAT_WIDTH = 8


def init_colors() -> None:
    """Initialize all curses color pairs."""
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(PAIR_TITLE, curses.COLOR_CYAN, -1)
    curses.init_pair(PAIR_ACCENT, curses.COLOR_YELLOW, -1)
    curses.init_pair(PAIR_DIM, 8, -1)  # dark gray where supported
    curses.init_pair(PAIR_BODY, curses.COLOR_WHITE, -1)
    curses.init_pair(PAIR_SUCCESS, curses.COLOR_GREEN, -1)
    curses.init_pair(PAIR_WARN, curses.COLOR_RED, -1)
    curses.init_pair(PAIR_QOREX, curses.COLOR_WHITE, -1)
