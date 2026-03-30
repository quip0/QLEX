"""Main TUI app entry point for QLEX."""

from __future__ import annotations

import curses
import json
import os
import time
import traceback
from pathlib import Path

from qlex.registry import Registry
from qlex.ui.renderer import animate_transition
from qlex.ui.screens import (
    render_browse,
    render_compare,
    render_detail,
    render_help,
    render_splash,
)
from qlex.ui.state import Screen, UIState
from qlex.ui.theme import ANIM_FPS, init_colors


def _log_error(error: Exception) -> None:
    """Log an error to ~/.qlex/error.log."""
    log_dir = Path.home() / ".qlex"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "error.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {type(error).__name__}: {error}\n")
        f.write(traceback.format_exc())
        f.write("\n")


def _get_filtered_codes(reg: Registry, state: UIState) -> list:
    """Return codes filtered by current UI state."""
    if state.search_mode and state.search_query:
        codes = reg.search(state.search_query)
    elif state.filter_family:
        codes = reg.filter(family=state.filter_family)
    else:
        codes = reg.list_codes()
    return codes


def _main(stdscr: curses.window) -> None:
    """Inner main function running under curses.wrapper."""
    # Check terminal size
    max_y, max_x = stdscr.getmaxyx()
    if max_x < 80 or max_y < 24:
        stdscr.erase()
        msg = f"QLEX requires a terminal at least 80×24. Current: {max_x}×{max_y}"
        try:
            stdscr.addstr(0, 0, msg)
        except curses.error:
            pass
        stdscr.refresh()
        stdscr.getch()
        return

    # Initialize
    curses.curs_set(0)
    init_colors()
    stdscr.timeout(1000 // ANIM_FPS)
    stdscr.keypad(True)

    state = UIState()
    reg = Registry()
    splash_start = time.time()
    all_families = reg.families()

    while True:
        try:
            max_y, max_x = stdscr.getmaxyx()
            if max_x < 80 or max_y < 24:
                stdscr.erase()
                msg = f"QLEX requires a terminal at least 80×24. Current: {max_x}×{max_y}"
                try:
                    stdscr.addstr(0, 0, msg)
                except curses.error:
                    pass
                stdscr.refresh()
                ch = stdscr.getch()
                if ch == ord("q") or ch == 3:  # ctrl+c
                    break
                continue

            # Animate transitions
            if state.should_animate:
                animate_transition(stdscr, "forward")
                state.should_animate = False

            # Render current screen
            if state.current_screen == Screen.SPLASH:
                done = render_splash(stdscr, state, splash_start)
                if done:
                    state.transition_to(Screen.BROWSE)
                    continue
                ch = stdscr.getch()
                if ch == ord("q") or ch == 3:
                    break
                if ch != -1:
                    state.transition_to(Screen.BROWSE)
                continue

            codes = _get_filtered_codes(reg, state)

            if state.current_screen == Screen.BROWSE:
                # Clamp selection
                if codes:
                    state.selected_index = max(0, min(state.selected_index, len(codes) - 1))
                render_browse(stdscr, state, codes)

            elif state.current_screen == Screen.DETAIL:
                render_detail(stdscr, state)

            elif state.current_screen == Screen.COMPARE:
                render_compare(stdscr, state, reg.list_codes())

            elif state.current_screen == Screen.HELP:
                render_help(stdscr, state)

            # Input handling
            ch = stdscr.getch()
            if ch == -1:
                continue

            # Global: quit
            if ch == 3:  # ctrl+c
                break

            # Search mode input handling
            if state.search_mode:
                if ch == 27:  # ESC
                    state.search_mode = False
                    state.search_query = ""
                    state.selected_index = 0
                elif ch == 10 or ch == curses.KEY_ENTER:  # ENTER
                    state.search_mode = False
                    if codes:
                        state.active_code = codes[state.selected_index]
                        state.transition_to(Screen.DETAIL)
                elif ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8:
                    state.search_query = state.search_query[:-1]
                    state.selected_index = 0
                elif 32 <= ch <= 126:
                    state.search_query += chr(ch)
                    state.selected_index = 0
                continue

            # Screen-specific input
            if state.current_screen == Screen.BROWSE:
                if ch == ord("q"):
                    break
                elif ch == curses.KEY_UP or ch == ord("k"):
                    state.selected_index = max(0, state.selected_index - 1)
                elif ch == curses.KEY_DOWN or ch == ord("j"):
                    if codes:
                        state.selected_index = min(len(codes) - 1, state.selected_index + 1)
                elif ch == 10 or ch == curses.KEY_ENTER:  # ENTER
                    if codes:
                        state.active_code = codes[state.selected_index]
                        state.transition_to(Screen.DETAIL)
                elif ch == ord("/"):
                    state.search_mode = True
                    state.search_query = ""
                    state.selected_index = 0
                elif ch == ord("c"):
                    if codes:
                        code = codes[state.selected_index]
                        state.toggle_compare(code.id)
                elif ch == ord("C"):
                    if len(state.compare_selection) >= 2:
                        state.transition_to(Screen.COMPARE)
                    else:
                        state.set_message("Stage at least 2 codes with 'c' first")
                elif ch == ord("f"):
                    if state.filter_family is None:
                        state.filter_family = all_families[0] if all_families else None
                    else:
                        idx = all_families.index(state.filter_family)
                        if idx + 1 < len(all_families):
                            state.filter_family = all_families[idx + 1]
                        else:
                            state.filter_family = None
                    state.selected_index = 0
                elif ch == 27:  # ESC
                    state.filter_family = None
                    state.selected_index = 0
                elif ch == ord("?"):
                    state.transition_to(Screen.HELP)

            elif state.current_screen == Screen.DETAIL:
                if ch == 27 or ch == ord("b"):  # ESC or b
                    state.transition_to(Screen.BROWSE)
                elif ch == ord("c"):
                    if state.active_code:
                        state.toggle_compare(state.active_code.id)
                elif ch == ord("e"):
                    if state.active_code:
                        config = state.active_code.to_export_config()
                        json_str = json.dumps(config, indent=2)
                        # Show in an overlay
                        stdscr.erase()
                        lines = json_str.split("\n")
                        draw_y = 1
                        try:
                            stdscr.addstr(0, 1, "EXPORT CONFIG (press any key to close)", curses.A_BOLD)
                        except curses.error:
                            pass
                        for i, line in enumerate(lines):
                            if draw_y + i >= max_y - 1:
                                break
                            try:
                                stdscr.addstr(draw_y + i, 2, line)
                            except curses.error:
                                pass
                        stdscr.refresh()
                        stdscr.timeout(-1)
                        stdscr.getch()
                        stdscr.timeout(1000 // ANIM_FPS)

            elif state.current_screen == Screen.COMPARE:
                if ch == 27:  # ESC
                    state.transition_to(Screen.BROWSE)
                elif ch == ord("c"):
                    state.compare_selection.clear()
                    state.transition_to(Screen.BROWSE)

            elif state.current_screen == Screen.HELP:
                if ch == 27 or ch == ord("q"):
                    state.transition_to(Screen.BROWSE)

        except KeyboardInterrupt:
            break
        except Exception as e:
            _log_error(e)
            continue


def run() -> None:
    """Launch the QLEX terminal UI."""
    try:
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(_main)
    except KeyboardInterrupt:
        pass
    finally:
        print("QLEX — by Qorex")


if __name__ == "__main__":
    run()
