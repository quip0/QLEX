<p align="center">
  <img src="../assets/logos/qlex.svg" alt="QLEX" width="320" />
</p>

# Terminal UI Guide

The QLEX terminal UI is an interactive ASCII explorer for the QEC code registry. It is entirely keyboard-driven, uses animated transitions, and is built on Python's `curses` stdlib with zero external TUI dependencies.

---

## Launching

```bash
# Via the installed console script
qlex

# Or directly via Python
python -m qlex.ui.app
```

The TUI requires a terminal at least **80 columns by 24 rows**. If the terminal is too small, QLEX will display a size error and exit cleanly.

On exit (`q` or `Ctrl+C`), QLEX prints `"QLEX — by Qorex"` to stdout and restores the terminal.

---

## Screens

### SPLASH

<img src="../assets/logos/icon.svg" alt="QLEX" width="32" align="left" style="margin-right: 12px" />

The splash screen is shown for 2 seconds on launch. It displays the QLEX logo, the tagline *"The Quantum Lexicon"*, the Qorex brand mark, and an animated loading bar. Press any key to skip.

<br clear="all" />

---

### BROWSE

The main explorer where you spend most of your time.

```
 QLEX                               [family: topological]        4 codes
 ─────────────────────────────────────────────────────────────────────────
 CODES                       │  Surface Code
                              │  [[2d^2 - 1, 1, variable]]
    Color Code        [top.]  │
    Rotated Surface   [top.]  │  Circuit-level: ████████░░░░░░ 0.0057
  ▶ Surface Code      [top.]  │  Depolarizing:  █████████████░ 0.1890
    Toric Code        [top.]  │
                              │  Hardware:
                              │  [superconducting] [trapped_ion] ...
                              │
                              │  The surface code is a topological
                              │  stabilizer code defined on a 2D
                              │  lattice of qubits.
 ─────────────────────────────────────────────────────────────────────────
 ENTER detail · / search · c compare · C compare view · f filter · ? help
```

**Layout:**
- **Top bar** — QLEX name on the left, active filter indicators in the center, code count on the right
- **Left panel (30%)** — Scrollable list of codes with `▶` cursor. Each item shows the code name and a family tag. Codes staged for comparison show a `◆` marker instead
- **Right panel (70%)** — Live preview of the selected code: name, [[n,k,d]] parameters, threshold bars, hardware tags, and the first two sentences of the description
- **Footer** — Keyboard hint or status message

**Keyboard:**

| Key | Action |
|-----|--------|
| `↑` / `k` | Move selection up |
| `↓` / `j` | Move selection down |
| `Enter` | Open DETAIL for selected code |
| `/` | Enter SEARCH mode |
| `c` | Toggle selected code into compare selection (max 3) |
| `C` | Open COMPARE screen (requires 2+ staged codes) |
| `f` | Cycle through family filters (topological → CSS → ... → none) |
| `Esc` | Clear active filters |
| `?` | Open HELP screen |
| `q` | Quit QLEX |

---

### DETAIL

Full-page view of a single QEC code. All properties are displayed in a two-column layout.

```
 ← BROWSE                    Surface Code                     [topological]
 ─────────────────────────────────────────────────────────────────────────
 PARAMETERS                  │ DESCRIPTION
   n = 2d^2 - 1              │ The surface code is a topological
   k = 1                     │ stabilizer code defined on a 2D lattice
   d = variable              │ of qubits. It achieves high error
                              │ thresholds due to local stabilizer
 THRESHOLDS                  │ checks and is a leading candidate ...
   Circuit-level: ████ 0.0057│
   Depolarizing:  ████ 0.1890│ DECODERS
                              │ MWPM, Union-Find, Belief Propagation
 HARDWARE                    │
   [superconducting]          │ NOISE MODELS
   [trapped_ion]              │ depolarizing, biased, erasure, ...
   [neutral_atom]             │
                              │ KEY PAPERS
 CONNECTIVITY                │ Dennis, Kitaev et al. (2002)
   2D nearest-neighbor grid   │   Topological quantum memory
                              │   arxiv: quant-ph/0110143
 ─────────────────────────────────────────────────────────────────────────
 ESC back · c stage for compare · e export config
```

**Left column:** Parameters, thresholds with ASCII bars, hardware tags, connectivity.

**Right column:** Description, decoders, noise models, logical gates, key papers with citations.

**Keyboard:**

| Key | Action |
|-----|--------|
| `Esc` / `b` | Return to BROWSE (restores previous selection) |
| `c` | Stage this code for comparison |
| `e` | Export config — shows JSON in a modal overlay (press any key to close) |

---

### SEARCH

Search is an overlay on the BROWSE screen, not a separate screen. It activates a search bar at the bottom.

```
 / surface█
```

**Behavior:**
- The code list filters in real time on every keypress
- The preview panel updates to show the first matching result
- If no codes match, the list panel shows `"no codes matched"` in red

**Keyboard:**

| Key | Action |
|-----|--------|
| Type | Characters are appended to the search query |
| `Backspace` | Delete last character |
| `Enter` | Select the first result and open DETAIL |
| `Esc` | Cancel search and return to full list |

---

### COMPARE

Side-by-side comparison of 2 or 3 staged codes.

```
 COMPARE                    Surface Code vs Color Code
 ─────────────────────────────────────────────────────────────────────────
 Surface Code                        Color Code
 ─────────────────────────           ─────────────────────────
 Parameters:
   [[2d^2 - 1, 1, variable]]          [[18, 1, 5]]

 Circuit-level threshold:
   ████████░░░░ 0.0057                ██████░░░░░░ 0.0046

 Depolarizing threshold:
   █████████████░ 0.1890              ████████░░░░░░ 0.1090

 Hardware:
   [superconducting] [trapped_ion]    [superconducting] [trapped_ion]

 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WINNERS
   circuit_level_threshold: ██ Surface Code
   depolarizing_threshold:  ██ Surface Code
   qubit_efficiency:        ── no data
 ─────────────────────────────────────────────────────────────────────────
 ESC back · c clear selection
```

The bottom section highlights the winner for each metric. Metrics that can't be determined show `"── no data"`.

**Keyboard:**

| Key | Action |
|-----|--------|
| `Esc` | Return to BROWSE |
| `c` | Clear compare selection and return to BROWSE |

---

### HELP

Full-screen keyboard reference with all bindings grouped by screen context.

**Keyboard:**

| Key | Action |
|-----|--------|
| `Esc` / `q` | Close help and return to BROWSE |

---

## Design Principles

- **No mouse.** Entirely keyboard-driven.
- **No external TUI frameworks.** Built on Python's `curses` stdlib directly.
- **Fluid transitions.** Screen changes animate with a character-density dissolve effect using `█▓▒░ `.
- **ASCII-native.** All visual elements use Unicode box-drawing characters. The UI is readable in monochrome; colors enhance it when supported.
- **Game-feel.** Navigation feels like exploring a system, not reading documentation.

---

## Terminal Requirements

- Minimum size: **80 columns x 24 rows**
- Color support: Optional but recommended (256-color or truecolor terminal)
- Tested on: macOS Terminal, iTerm2, Alacritty, Kitty, Windows Terminal, GNOME Terminal

---

## Error Logging

If an unexpected error occurs during the TUI session, it is logged to `~/.qlex/error.log` and the TUI continues running. The main event loop never crashes on unexpected input.

---

<p align="center">
  <img src="../assets/logos/icon.svg" alt="QLEX" width="48" />
  <br />
  <sub>QLEX is a product of <a href="https://github.com/qorex">Qorex</a></sub>
</p>
