"""ASCII rendering primitives for the QLEX terminal UI."""

from __future__ import annotations

import curses
import time

from qlex.ui.theme import (
    ANIM_FPS,
    ANIM_TRANSITION_FRAMES,
    BRAND,
    CHAR_DENSITY,
    LOGO,
    PAIR_DIM,
    PAIR_QOREX,
    PAIR_TITLE,
)


def _safe_addstr(win: curses.window, y: int, x: int, text: str, attr: int = 0) -> None:
    """Write text to window, clipping to bounds without raising errors."""
    max_y, max_x = win.getmaxyx()
    if y < 0 or y >= max_y or x >= max_x:
        return
    available = max_x - x
    if available <= 0:
        return
    clipped = text[:available]
    try:
        win.addstr(y, x, clipped, attr)
    except curses.error:
        pass


def draw_box(
    win: curses.window,
    y: int,
    x: int,
    h: int,
    w: int,
    glyphs: dict[str, str],
    color_pair: int,
    title: str | None = None,
) -> None:
    """Draw a box with optional centered title in the top border."""
    attr = curses.color_pair(color_pair)
    # Top border
    _safe_addstr(win, y, x, glyphs["tl"] + glyphs["h"] * (w - 2) + glyphs["tr"], attr)
    if title:
        title_str = f" {title} "
        tx = x + (w - len(title_str)) // 2
        _safe_addstr(win, y, tx, title_str, attr | curses.A_BOLD)
    # Sides
    for row in range(1, h - 1):
        _safe_addstr(win, y + row, x, glyphs["v"], attr)
        _safe_addstr(win, y + row, x + w - 1, glyphs["v"], attr)
    # Bottom border
    _safe_addstr(win, y + h - 1, x, glyphs["bl"] + glyphs["h"] * (w - 2) + glyphs["br"], attr)


def draw_hline(
    win: curses.window,
    y: int,
    x: int,
    w: int,
    glyphs: dict[str, str],
    color_pair: int,
) -> None:
    """Draw a horizontal rule."""
    attr = curses.color_pair(color_pair)
    _safe_addstr(win, y, x, glyphs["h"] * w, attr)


def draw_logo(win: curses.window, y: int, x: int) -> None:
    """Render the QLEX ASCII logo."""
    attr = curses.color_pair(PAIR_TITLE) | curses.A_BOLD
    for i, line in enumerate(LOGO):
        _safe_addstr(win, y + i, x, line, attr)


def draw_brand(win: curses.window, y: int, x: int) -> None:
    """Render 'by Qorex' in PAIR_QOREX."""
    attr = curses.color_pair(PAIR_QOREX) | curses.A_BOLD
    _safe_addstr(win, y, x, BRAND, attr)


def draw_text(
    win: curses.window,
    y: int,
    x: int,
    text: str,
    color_pair: int,
    bold: bool = False,
) -> None:
    """Draw text at position with color, clipping to window bounds."""
    attr = curses.color_pair(color_pair)
    if bold:
        attr |= curses.A_BOLD
    _safe_addstr(win, y, x, text, attr)


def draw_scrollable_list(
    win: curses.window,
    y: int,
    x: int,
    h: int,
    w: int,
    items: list[str],
    selected_idx: int,
    color_pair_normal: int,
    color_pair_selected: int,
) -> int:
    """Render a scrollable list with cursor. Returns the scroll offset used."""
    if not items:
        return 0

    # Calculate scroll offset
    scroll_offset = 0
    if selected_idx >= h:
        scroll_offset = selected_idx - h + 1
    if scroll_offset > len(items) - h:
        scroll_offset = max(0, len(items) - h)

    visible = items[scroll_offset:scroll_offset + h]
    for i, item in enumerate(visible):
        actual_idx = scroll_offset + i
        truncated = item[:w]
        if actual_idx == selected_idx:
            attr = curses.color_pair(color_pair_selected) | curses.A_BOLD
            # Highlight the full line
            _safe_addstr(win, y + i, x, " " * w, attr)
            _safe_addstr(win, y + i, x, truncated, attr)
        else:
            attr = curses.color_pair(color_pair_normal)
            _safe_addstr(win, y + i, x, truncated, attr)

    # Scroll indicators
    if scroll_offset > 0:
        _safe_addstr(win, y, x + w - 1, "▲", curses.color_pair(PAIR_DIM))
    if scroll_offset + h < len(items):
        _safe_addstr(win, y + h - 1, x + w - 1, "▼", curses.color_pair(PAIR_DIM))

    return scroll_offset


def draw_tag(win: curses.window, y: int, x: int, text: str, color_pair: int) -> int:
    """Render a tag as [text]. Returns the width consumed."""
    tag_str = f"[{text}]"
    _safe_addstr(win, y, x, tag_str, curses.color_pair(color_pair))
    return len(tag_str)


def draw_threshold_bar(
    win: curses.window,
    y: int,
    x: int,
    w: int,
    value: float | None,
    max_value: float,
    color_pair: int,
) -> None:
    """Render a horizontal ASCII bar chart: ████░░░░ 0.57%."""
    if value is None:
        _safe_addstr(win, y, x, "────  N/A", curses.color_pair(6))  # PAIR_WARN
        return

    bar_w = max(w - 10, 4)
    fill = int((value / max_value) * bar_w) if max_value > 0 else 0
    fill = min(fill, bar_w)
    empty = bar_w - fill
    bar = "█" * fill + "░" * empty
    label = f" {value:.4f}"
    _safe_addstr(win, y, x, bar, curses.color_pair(color_pair))
    _safe_addstr(win, y, x + bar_w, label, curses.color_pair(color_pair))


def animate_transition(win: curses.window, direction: str = "forward") -> None:
    """Wipe screen content using CHAR_DENSITY for a dissolve effect."""
    max_y, max_x = win.getmaxyx()
    delay = 1.0 / ANIM_FPS

    density_seq = CHAR_DENSITY if direction == "forward" else CHAR_DENSITY[::-1]

    for frame in range(ANIM_TRANSITION_FRAMES):
        char_idx = int((frame / ANIM_TRANSITION_FRAMES) * (len(density_seq) - 1))
        ch = density_seq[char_idx]
        attr = curses.color_pair(PAIR_DIM)
        for row in range(max_y - 1):
            try:
                win.addstr(row, 0, ch * (max_x - 1), attr)
            except curses.error:
                pass
        win.refresh()
        time.sleep(delay)

    win.erase()
    win.refresh()


def animate_cursor_blink(win: curses.window, y: int, x: int, char: str = "█") -> None:
    """Render a blinking cursor using time-based toggle."""
    show = int(time.time() * 3) % 2 == 0
    if show:
        _safe_addstr(win, y, x, char, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    else:
        _safe_addstr(win, y, x, " ", 0)
