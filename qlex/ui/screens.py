"""Individual screen render functions for the QLEX terminal UI."""

from __future__ import annotations

import curses
import time

from qlex.compare import Comparison
from qlex.exceptions import ComparisonError
from qlex.models import QECCode
from qlex.ui.renderer import (
    animate_cursor_blink,
    draw_box,
    draw_brand,
    draw_hline,
    draw_logo,
    draw_scrollable_list,
    draw_tag,
    draw_text,
    draw_threshold_bar,
    get_cat_region,
)
from qlex.ui.state import UIState
from qlex.ui.theme import (
    GLYPHS_HEAVY,
    GLYPHS_LIGHT,
    LOGO,
    PAIR_ACCENT,
    PAIR_BODY,
    PAIR_DIM,
    PAIR_QOREX,
    PAIR_SUCCESS,
    PAIR_TITLE,
    PAIR_WARN,
)


def _word_wrap(text: str, width: int) -> list[str]:
    """Wrap text to fit within the given width."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        elif current:
            current += " " + word
        else:
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def render_splash(win: curses.window, state: UIState, start_time: float) -> bool:
    """Render the SPLASH screen. Returns True when splash is complete."""
    max_y, max_x = win.getmaxyx()
    win.erase()

    # Center the logo
    logo_h = len(LOGO)
    logo_w = max(len(line) for line in LOGO)
    cy = (max_y - logo_h - 6) // 2
    cx = (max_x - logo_w) // 2

    draw_logo(win, cy, cx)

    # Tagline
    tagline = "The Quantum Lexicon"
    draw_text(win, cy + logo_h + 1, (max_x - len(tagline)) // 2, tagline, PAIR_DIM)

    # Brand
    brand = "by Qorex"
    draw_text(win, cy + logo_h + 3, (max_x - len(brand)) // 2, brand, PAIR_QOREX, bold=True)

    # Loading bar
    elapsed = time.time() - start_time
    progress = min(elapsed / 2.0, 1.0)
    bar_w = 30
    bar_x = (max_x - bar_w) // 2
    bar_y = cy + logo_h + 5
    filled = int(progress * bar_w)
    bar = "█" * filled + "░" * (bar_w - filled)
    draw_text(win, bar_y, bar_x, bar, PAIR_TITLE)

    return progress >= 1.0


def render_browse(
    win: curses.window,
    state: UIState,
    codes: list[QECCode],
) -> None:
    """Render the BROWSE screen with code list and live preview."""
    max_y, max_x = win.getmaxyx()
    win.erase()

    # Top bar
    draw_text(win, 0, 1, "QLEX", PAIR_TITLE, bold=True)

    # Filter indicators in center
    if state.filter_family:
        filter_str = f"[family: {state.filter_family}]"
        draw_text(win, 0, (max_x - len(filter_str)) // 2, filter_str, PAIR_ACCENT)

    # Code count on right
    count_str = f"{len(codes)} codes"
    draw_text(win, 0, max_x - len(count_str) - 1, count_str, PAIR_TITLE)

    draw_hline(win, 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    # Split: left panel 30%, right panel 70%
    left_w = max(20, max_x * 30 // 100)
    right_x = left_w + 1
    right_w = max_x - right_x - 1
    content_h = max_y - 4  # top bar + hline + footer + status

    # Left panel - scrollable code list
    draw_text(win, 2, 1, "CODES", PAIR_DIM)
    # Vertical divider
    for row in range(2, 2 + content_h):
        draw_text(win, row, left_w, "│", PAIR_DIM)

    items = []
    for code in codes:
        family_tag = f"[{code.family}]"
        name_w = left_w - len(family_tag) - 5
        name = code.name[:name_w] if len(code.name) > name_w else code.name
        padding = left_w - 4 - len(name) - len(family_tag)
        # Mark compared codes
        marker = "◆" if code.id in state.compare_selection else "▶"
        items.append(f" {marker} {name}{' ' * max(1, padding)}{family_tag}")

    cat_top_y = get_cat_region(max_y)[0]
    list_h = min(content_h - 1, cat_top_y - 3)
    draw_scrollable_list(
        win, 3, 0, list_h, left_w, items,
        state.selected_index, PAIR_BODY, PAIR_ACCENT,
    )

    # Right panel - live preview
    if codes and 0 <= state.selected_index < len(codes):
        code = codes[state.selected_index]
        ry = 2
        draw_text(win, ry, right_x + 1, code.name, PAIR_TITLE, bold=True)
        ry += 1

        params = f"[[{code.parameters.n}, {code.parameters.k}, {code.parameters.d}]]"
        draw_text(win, ry, right_x + 1, params, PAIR_BODY)
        ry += 2

        # Thresholds
        draw_text(win, ry, right_x + 1, "Circuit-level:", PAIR_DIM)
        draw_threshold_bar(win, ry, right_x + 17, right_w - 18, code.threshold.circuit_level, 0.02, PAIR_SUCCESS)
        ry += 1
        draw_text(win, ry, right_x + 1, "Depolarizing: ", PAIR_DIM)
        draw_threshold_bar(win, ry, right_x + 17, right_w - 18, code.threshold.depolarizing, 0.20, PAIR_SUCCESS)
        ry += 2

        # Hardware tags
        draw_text(win, ry, right_x + 1, "Hardware:", PAIR_DIM)
        ry += 1
        tx = right_x + 1
        for hw in code.hardware_compatibility:
            tag_w = draw_tag(win, ry, tx, hw, PAIR_ACCENT)
            tx += tag_w + 1
            if tx + 10 > max_x:
                ry += 1
                tx = right_x + 1
        ry += 2

        # Description (first 2 sentences)
        desc = code.description
        sentences = desc.split(". ")
        short_desc = ". ".join(sentences[:2])
        if len(sentences) > 2:
            short_desc += "."
        for line in _word_wrap(short_desc, right_w - 2):
            draw_text(win, ry, right_x + 1, line, PAIR_BODY)
            ry += 1

    # Footer
    footer_y = max_y - 2
    draw_hline(win, footer_y, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    if state.search_mode:
        search_str = f"/ {state.search_query}"
        draw_text(win, footer_y + 1, 1, search_str, PAIR_TITLE)
        animate_cursor_blink(win, footer_y + 1, 1 + len(search_str) + 1, "█")
    else:
        msg = state.get_message()
        if msg:
            draw_text(win, footer_y + 1, 1, msg, PAIR_ACCENT)
        else:
            hint = "ENTER detail · / search · c compare · C compare view · d describe · f filter · ? help · q quit"
            draw_text(win, footer_y + 1, 1, hint[:max_x - 2], PAIR_DIM)


def render_detail(win: curses.window, state: UIState) -> None:
    """Render the DETAIL screen for a single QEC code."""
    max_y, max_x = win.getmaxyx()
    win.erase()
    code = state.active_code
    if code is None:
        return

    # Header
    draw_text(win, 0, 1, "← BROWSE", PAIR_DIM)
    draw_text(win, 0, (max_x - len(code.name)) // 2, code.name, PAIR_TITLE, bold=True)
    family_tag = f"[{code.family}]"
    draw_text(win, 0, max_x - len(family_tag) - 1, family_tag, PAIR_ACCENT)
    draw_hline(win, 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    # Two columns
    col_w = (max_x - 3) // 2
    left_x = 1
    right_x = col_w + 3

    # Vertical divider
    for row in range(2, max_y - 2):
        draw_text(win, row, col_w + 1, "│", PAIR_DIM)

    # LEFT COLUMN — stop before the cat region
    ly = 2
    cat_top_y = get_cat_region(max_y)[0]

    # Parameters section
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "PARAMETERS", PAIR_TITLE, bold=True)
        ly += 1
    if ly < cat_top_y:
        draw_text(win, ly, left_x, f"  n = {code.parameters.n}", PAIR_BODY)
        ly += 1
    if ly < cat_top_y:
        draw_text(win, ly, left_x, f"  k = {code.parameters.k}", PAIR_BODY)
        ly += 1
    if ly < cat_top_y:
        draw_text(win, ly, left_x, f"  d = {code.parameters.d}", PAIR_BODY)
        ly += 2

    # Thresholds section
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "THRESHOLDS", PAIR_TITLE, bold=True)
        ly += 1
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "  Circuit-level:", PAIR_DIM)
        draw_threshold_bar(win, ly, left_x + 18, col_w - 20, code.threshold.circuit_level, 0.02, PAIR_SUCCESS)
        ly += 1
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "  Depolarizing: ", PAIR_DIM)
        draw_threshold_bar(win, ly, left_x + 18, col_w - 20, code.threshold.depolarizing, 0.20, PAIR_SUCCESS)
        ly += 2

    # Hardware section
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "HARDWARE", PAIR_TITLE, bold=True)
        ly += 1
    if ly < cat_top_y:
        tx = left_x + 2
        for hw in code.hardware_compatibility:
            if ly >= cat_top_y:
                break
            tag_w = draw_tag(win, ly, tx, hw, PAIR_ACCENT)
            tx += tag_w + 1
            if tx + 10 > left_x + col_w:
                ly += 1
                tx = left_x + 2
        ly += 2

    # Connectivity
    if ly < cat_top_y:
        draw_text(win, ly, left_x, "CONNECTIVITY", PAIR_TITLE, bold=True)
        ly += 1
    for line in _word_wrap(code.connectivity, col_w - 4):
        if ly >= cat_top_y:
            break
        draw_text(win, ly, left_x + 2, line, PAIR_BODY)
        ly += 1

    # RIGHT COLUMN
    ry = 2

    # Description
    draw_text(win, ry, right_x, "DESCRIPTION", PAIR_TITLE, bold=True)
    ry += 1
    for line in _word_wrap(code.description, col_w - 2):
        if ry >= max_y - 2:
            break
        draw_text(win, ry, right_x, line, PAIR_BODY)
        ry += 1
    ry += 1

    # Decoders
    if ry < max_y - 6:
        draw_text(win, ry, right_x, "DECODERS", PAIR_TITLE, bold=True)
        ry += 1
        draw_text(win, ry, right_x, ", ".join(code.decoders) if code.decoders else "None", PAIR_BODY)
        ry += 2

    # Noise Models
    if ry < max_y - 6:
        draw_text(win, ry, right_x, "NOISE MODELS", PAIR_TITLE, bold=True)
        ry += 1
        draw_text(win, ry, right_x, ", ".join(code.noise_models) if code.noise_models else "None", PAIR_BODY)
        ry += 2

    # Logical Gates
    if ry < max_y - 6:
        draw_text(win, ry, right_x, "LOGICAL GATES", PAIR_TITLE, bold=True)
        ry += 1
        gates_str = ", ".join(code.logical_gates) if code.logical_gates else "None"
        for line in _word_wrap(gates_str, col_w - 2):
            if ry >= max_y - 4:
                break
            draw_text(win, ry, right_x, line, PAIR_BODY)
            ry += 1
        ry += 1

    # Key Papers
    if ry < max_y - 4 and code.key_papers:
        draw_text(win, ry, right_x, "KEY PAPERS", PAIR_TITLE, bold=True)
        ry += 1
        for p in code.key_papers:
            if ry >= max_y - 3:
                break
            authors = ", ".join(p.authors[:2])
            if len(p.authors) > 2:
                authors += " et al."
            line = f"{authors} ({p.year})"
            draw_text(win, ry, right_x, line[:col_w - 2], PAIR_BODY)
            ry += 1
            title_line = f"  {p.title}"
            draw_text(win, ry, right_x, title_line[:col_w - 2], PAIR_DIM)
            ry += 1
            draw_text(win, ry, right_x, f"  arxiv: {p.arxiv}", PAIR_DIM)
            ry += 1

    # Footer
    footer_y = max_y - 1
    draw_hline(win, footer_y - 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)
    msg = state.get_message()
    if msg:
        draw_text(win, footer_y, 1, msg, PAIR_ACCENT)
    else:
        draw_text(win, footer_y, 1, "ESC back · c stage for compare · d describe fields · e export config", PAIR_DIM)


def render_compare(win: curses.window, state: UIState, codes: list[QECCode]) -> None:
    """Render the COMPARE screen with side-by-side code comparison."""
    max_y, max_x = win.getmaxyx()
    win.erase()

    compare_codes = [c for c in codes if c.id in state.compare_selection]
    if len(compare_codes) < 2:
        draw_text(win, max_y // 2, (max_x - 30) // 2, "Need at least 2 codes to compare", PAIR_WARN)
        draw_text(win, max_y // 2 + 2, (max_x - 20) // 2, "ESC to go back", PAIR_DIM)
        win.refresh()
        return

    # Header
    names = " vs ".join(c.name for c in compare_codes)
    draw_text(win, 0, 1, "COMPARE", PAIR_TITLE, bold=True)
    draw_text(win, 0, 10, names[:max_x - 12], PAIR_BODY)
    draw_hline(win, 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    num_cols = len(compare_codes)
    col_w = (max_x - 2) // num_cols

    # Column headers
    for i, code in enumerate(compare_codes):
        cx = 1 + i * col_w
        draw_text(win, 2, cx, code.name[:col_w - 2], PAIR_ACCENT, bold=True)
        draw_hline(win, 3, cx, col_w - 1, GLYPHS_LIGHT, PAIR_DIM)

    # Rows of comparison data
    def _draw_row(y: int, label: str, values: list[str]) -> int:
        draw_text(win, y, 1, label, PAIR_DIM)
        y += 1
        for i, val in enumerate(values):
            cx = 1 + i * col_w
            draw_text(win, y, cx + 2, val[:col_w - 4], PAIR_BODY)
        return y + 1

    ry = 4
    ry = _draw_row(ry, "Parameters:", [
        f"[[{c.parameters.n}, {c.parameters.k}, {c.parameters.d}]]" for c in compare_codes
    ])
    ry += 1

    ry = _draw_row(ry, "Family:", [c.family for c in compare_codes])
    ry += 1

    # Thresholds with bars
    draw_text(win, ry, 1, "Circuit-level threshold:", PAIR_DIM)
    ry += 1
    for i, code in enumerate(compare_codes):
        cx = 1 + i * col_w
        draw_threshold_bar(win, ry, cx + 2, col_w - 6, code.threshold.circuit_level, 0.02, PAIR_SUCCESS)
    ry += 2

    draw_text(win, ry, 1, "Depolarizing threshold:", PAIR_DIM)
    ry += 1
    for i, code in enumerate(compare_codes):
        cx = 1 + i * col_w
        draw_threshold_bar(win, ry, cx + 2, col_w - 6, code.threshold.depolarizing, 0.20, PAIR_SUCCESS)
    ry += 2

    # Hardware tags
    draw_text(win, ry, 1, "Hardware:", PAIR_DIM)
    ry += 1
    for i, code in enumerate(compare_codes):
        cx = 1 + i * col_w
        tx = cx + 2
        for hw in code.hardware_compatibility[:4]:
            tw = draw_tag(win, ry, tx, hw, PAIR_ACCENT)
            tx += tw + 1
            if tx > cx + col_w - 4:
                break
    ry += 2

    # Decoders
    ry = _draw_row(ry, "Decoders:", [
        ", ".join(c.decoders[:3]) for c in compare_codes
    ])
    ry += 1

    # Winner section
    if ry < max_y - 5:
        draw_hline(win, ry, 0, max_x, GLYPHS_HEAVY, PAIR_DIM)
        ry += 1
        draw_text(win, ry, 1, "WINNERS", PAIR_TITLE, bold=True)
        ry += 1

        try:
            comp = Comparison(compare_codes)
        except ComparisonError:
            comp = None

        for metric in ("circuit_level_threshold", "depolarizing_threshold", "qubit_efficiency"):
            if ry >= max_y - 2:
                break
            try:
                winner_id = comp.winner(metric) if comp else None
                winner_name = next((c.name for c in compare_codes if c.id == winner_id), "?")
                draw_text(win, ry, 3, f"{metric}: ", PAIR_DIM)
                draw_text(win, ry, 3 + len(metric) + 2, f"██ {winner_name}", PAIR_SUCCESS)
            except ComparisonError:
                draw_text(win, ry, 3, f"{metric}: ", PAIR_DIM)
                draw_text(win, ry, 3 + len(metric) + 2, "── no data", PAIR_WARN)
            ry += 1

    # Footer
    footer_y = max_y - 1
    draw_hline(win, footer_y - 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)
    draw_text(win, footer_y, 1, "ESC back · c clear selection", PAIR_DIM)


def render_help(win: curses.window, state: UIState) -> None:
    """Render the HELP screen with keyboard reference."""
    max_y, max_x = win.getmaxyx()
    win.erase()

    draw_text(win, 0, (max_x - 9) // 2, "QLEX HELP", PAIR_TITLE, bold=True)
    draw_hline(win, 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    col_w = (max_x - 4) // 2
    left_x = 2
    right_x = left_x + col_w + 2

    # Left column
    ly = 3
    draw_text(win, ly, left_x, "BROWSE", PAIR_TITLE, bold=True)
    ly += 1
    bindings_browse = [
        ("↑ / k", "Move selection up"),
        ("↓ / j", "Move selection down"),
        ("ENTER", "View code detail"),
        ("/", "Enter search mode"),
        ("c", "Stage code for compare"),
        ("C", "Open compare view"),
        ("f", "Cycle family filter"),
        ("ESC", "Clear filters"),
        ("?", "Open this help screen"),
        ("q", "Quit QLEX"),
    ]
    for key, desc in bindings_browse:
        draw_text(win, ly, left_x, f"[{key}]", PAIR_ACCENT)
        draw_text(win, ly, left_x + 10, desc, PAIR_BODY)
        ly += 1

    ly += 1
    draw_text(win, ly, left_x, "SEARCH", PAIR_TITLE, bold=True)
    ly += 1
    bindings_search = [
        ("type", "Filter codes in real time"),
        ("ENTER", "Select first result"),
        ("ESC", "Cancel search"),
    ]
    for key, desc in bindings_search:
        draw_text(win, ly, left_x, f"[{key}]", PAIR_ACCENT)
        draw_text(win, ly, left_x + 10, desc, PAIR_BODY)
        ly += 1

    # Right column
    ry = 3
    draw_text(win, ry, right_x, "DETAIL", PAIR_TITLE, bold=True)
    ry += 1
    bindings_detail = [
        ("ESC / b", "Return to browse"),
        ("c", "Stage for compare"),
        ("e", "Export config as JSON"),
    ]
    for key, desc in bindings_detail:
        draw_text(win, ry, right_x, f"[{key}]", PAIR_ACCENT)
        draw_text(win, ry, right_x + 12, desc, PAIR_BODY)
        ry += 1

    ry += 1
    draw_text(win, ry, right_x, "COMPARE", PAIR_TITLE, bold=True)
    ry += 1
    bindings_compare = [
        ("ESC", "Return to browse"),
        ("c", "Clear selection & return"),
    ]
    for key, desc in bindings_compare:
        draw_text(win, ry, right_x, f"[{key}]", PAIR_ACCENT)
        draw_text(win, ry, right_x + 12, desc, PAIR_BODY)
        ry += 1

    # Footer
    footer_y = max_y - 1
    draw_hline(win, footer_y - 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)
    draw_text(win, footer_y, 1, "ESC to close", PAIR_DIM)


def render_describe(win: curses.window, state: UIState) -> None:
    """Render the DESCRIBE screen explaining each field of a QEC code entry."""
    max_y, max_x = win.getmaxyx()
    win.erase()

    draw_text(win, 0, (max_x - 21) // 2, "FIELD DESCRIPTIONS", PAIR_TITLE, bold=True)
    draw_hline(win, 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)

    col_w = (max_x - 3) // 2
    left_x = 2
    right_x = col_w + 3

    # Vertical divider
    for row in range(2, max_y - 2):
        draw_text(win, row, col_w + 1, "│", PAIR_DIM)

    entries_left = [
        ("PARAMETERS  [[n, k, d]]", [
            "The code's defining numbers.",
            "n — total physical qubits needed.",
            "k — logical qubits encoded (the",
            "    useful information capacity).",
            "d — code distance: how many qubit",
            "    errors it can detect/correct.",
            "    Higher d = better protection.",
        ]),
        ("THRESHOLDS", [
            "Maximum physical error rates the",
            "code can tolerate and still correct.",
            "Circuit-level — realistic gate and",
            "  measurement errors combined.",
            "Depolarizing — symmetric noise on",
            "  every qubit each round.",
            "Higher values = more forgiving.",
        ]),
        ("HARDWARE", [
            "Quantum computing platforms the code",
            "has been demonstrated or designed",
            "for (e.g. superconducting, trapped",
            "ion, neutral atom, photonic).",
        ]),
        ("CONNECTIVITY", [
            "Required physical qubit layout.",
            "Describes how qubits must be wired",
            "together — e.g. 2D nearest-neighbor",
            "grid, all-to-all, heavy-hex.",
        ]),
    ]

    entries_right = [
        ("DESCRIPTION", [
            "A technical overview of what the",
            "code is, how it works, and what",
            "makes it notable or useful.",
        ]),
        ("DECODERS", [
            "Algorithms that read error syndrome",
            "measurements and figure out what",
            "went wrong. Examples: MWPM (minimum",
            "weight perfect matching), Union-Find,",
            "belief propagation.",
        ]),
        ("NOISE MODELS", [
            "Types of noise the code has been",
            "analyzed or benchmarked against,",
            "e.g. depolarizing, biased, erasure,",
            "circuit-level.",
        ]),
        ("LOGICAL GATES", [
            "Gate operations that can be applied",
            "to the encoded logical qubits.",
            "A universal set (e.g. H, CNOT, T)",
            "means arbitrary quantum computation.",
        ]),
        ("KEY PAPERS", [
            "Foundational publications that",
            "introduced or significantly advanced",
            "this code. Includes arXiv links.",
        ]),
    ]

    ly = 2
    for title, lines in entries_left:
        if ly >= max_y - 3:
            break
        draw_text(win, ly, left_x, title, PAIR_ACCENT, bold=True)
        ly += 1
        for line in lines:
            if ly >= max_y - 3:
                break
            draw_text(win, ly, left_x + 1, line[:col_w - 3], PAIR_BODY)
            ly += 1
        ly += 1

    ry = 2
    for title, lines in entries_right:
        if ry >= max_y - 3:
            break
        draw_text(win, ry, right_x, title, PAIR_ACCENT, bold=True)
        ry += 1
        for line in lines:
            if ry >= max_y - 3:
                break
            draw_text(win, ry, right_x + 1, line[:col_w - 3], PAIR_BODY)
            ry += 1
        ry += 1

    # Footer
    footer_y = max_y - 1
    draw_hline(win, footer_y - 1, 0, max_x, GLYPHS_LIGHT, PAIR_DIM)
    draw_text(win, footer_y, 1, "ESC to close", PAIR_DIM)
