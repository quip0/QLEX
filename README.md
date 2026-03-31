<p align="center">
  <img src="assets/logos/qlex.svg" alt="QLEX" width="480" />
</p>

<h3 align="center">The Quantum Lexicon</h3>

<p align="center">
  QEC code registry and intelligence layer
  <br />
  <a href="#install">Install</a> · <a href="#quickstart">Quickstart</a> · <a href="#python-api">Python API</a> · <a href="#terminal-ui">Terminal UI</a> · <a href="#cli">CLI</a> · <a href="docs/api-reference.md">API Reference</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/python-≥3.10-green" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License" />
</p>

---

**QLEX** is a pip-installable Python library and interactive terminal experience that serves as the authoritative registry and query interface for Quantum Error Correction (QEC) codes. It is the first product from [Qorex](https://github.com/qorex) — a quantum computing infrastructure company.

QLEX does not simulate or decode quantum circuits. It knows everything *about* QEC codes so that other tools don't have to. It is the language layer — the lexicon — that the entire Qorex ecosystem speaks.

## Install

```bash
pip install qlex
```

[![PyPI](https://img.shields.io/pypi/v/qlex)](https://pypi.org/project/qlex/)

Requires Python 3.10+. The only runtime dependency is [Pydantic v2](https://docs.pydantic.dev/).

Or install from source:

```bash
git clone https://github.com/qorex/qlex.git
cd qlex
pip install .
```

## Quickstart

Get up and running in under a minute. QLEX gives you three ways to interact with the QEC code registry: Python, terminal UI, and CLI.

### 1. Python — look up a code and inspect it

```python
import qlex

code = qlex.get("surface")
print(code.name)                        # Surface Code
print(code.parameters)                  # n='2d^2 - 1' k=1 d='variable'
print(code.threshold.circuit_level)     # 0.0057
print(code.hardware_compatibility)      # ['superconducting', 'trapped_ion', ...]
```

### 2. Python — filter, search, and compare

```python
# Find all topological codes that work on trapped ions
codes = qlex.filter(family="topological", hardware="trapped_ion")
for c in codes:
    print(c.name)
# Color Code
# Rotated Surface Code
# Surface Code
# Toric Code

# Fuzzy search across names, descriptions, and tags
qlex.search("biased")                   # codes mentioning biased noise

# Compare two codes head-to-head
comp = qlex.compare("surface", "color")
print(comp.winner("circuit_level_threshold"))   # surface
print(comp.table())                             # formatted ASCII table
```

### 3. Python — export for downstream tools

```python
config = qlex.get("surface").to_export_config()
```

Returns a versioned dict that any Qorex tool can ingest:

```json
{
  "code_id": "surface",
  "code_name": "Surface Code",
  "parameters": {"n": "2d^2 - 1", "k": 1, "d": "variable"},
  "supported_noise_models": ["depolarizing", "biased", "erasure", "circuit_level", "amplitude_damping"],
  "recommended_decoders": ["MWPM", "Union-Find", "Belief Propagation", "Neural Network"],
  "threshold_reference": {"depolarizing": 0.189, "circuit_level": 0.0057, "notes": "..."},
  "qlex_version": "0.1.0"
}
```

### 4. Terminal UI — explore interactively

```bash
qlex
```

Opens a keyboard-driven ASCII explorer with animated transitions, real-time search, and side-by-side comparison. Use `↑`/`↓` to browse, `/` to search, `c` to stage codes for comparison, `Enter` for detail, `d` for field descriptions. Press `?` for the full keyboard reference.

### 5. CLI — script and pipe

```bash
qlex list                                    # all codes
qlex get surface                             # full detail
qlex search biased                           # substring search
qlex compare surface color                   # comparison table
qlex export surface                          # JSON config for tooling
qlex filter --family topological --fault-tolerant   # combined filters
qlex export surface | jq '.recommended_decoders'    # pipe into jq
```

---

## Python API

```python
import qlex

# Look up a code by ID
surface = qlex.get("surface")
print(surface.summary())

# List everything in the registry
all_codes = qlex.list_codes()          # sorted alphabetically
print(qlex.count(), "codes across", qlex.families())

# Filter codes
topological = qlex.filter(family="topological")
ft_sc = qlex.filter(fault_tolerant=True, hardware="superconducting")
css_stab = qlex.filter(tags=["CSS", "stabilizer"])

# Search (case-insensitive substring across name, description, tags, noise models)
results = qlex.search("surface")       # Surface Code, Rotated Surface Code, ...

# Compare codes side-by-side
comp = qlex.compare("surface", "color", "steane")
print(comp.table())
print(comp.winner("circuit_level_threshold"))

# Export for downstream Qorex tools
config = surface.to_export_config()
# {
#   "code_id": "surface",
#   "code_name": "Surface Code",
#   "parameters": {"n": "2d^2 - 1", "k": 1, "d": "variable"},
#   "supported_noise_models": ["depolarizing", "biased", ...],
#   "recommended_decoders": ["MWPM", "Union-Find", ...],
#   "threshold_reference": {"depolarizing": 0.189, "circuit_level": 0.0057, ...},
#   "qlex_version": "0.1.0"
# }
```

See the full [API Reference](docs/api-reference.md) for detailed documentation.

## Terminal UI

```bash
qlex
```

The TUI is an entirely keyboard-driven ASCII explorer built on Python's `curses` stdlib — no external TUI frameworks. It features animated screen transitions, real-time search, threshold bar charts, and side-by-side code comparison.

```
 ┌──────────────────────────────────────────────────────────────────────────────┐
 │ QLEX                                                        9 codes        │
 ├──────────────────────────────┬───────────────────────────────────────────────┤
 │ CODES                       │  Surface Code                                │
 │                              │  [[2d^2 - 1, 1, variable]]                  │
 │    Bacon-Shor Code  [sub.]  │                                              │
 │    Color Code        [top.]  │  Circuit-level: ████████░░░░░░ 0.0057       │
 │    Gross [[144,12..  [qLD.]  │  Depolarizing:  █████████████░ 0.1890       │
 │    Repetition Code   [sta.]  │                                              │
 │    Rotated Surface   [top.]  │  Hardware:                                   │
 │    Shor [[9,1,3]]    [sta.]  │  [superconducting] [trapped_ion]            │
 │    Steane [[7,1,3]]  [CSS ]  │  [neutral_atom] [NV_center]                 │
 │  ▶ Surface Code      [top.]  │                                              │
 │    Toric Code        [top.]  │  The surface code is a topological           │
 │                              │  stabilizer code defined on a 2D lattice     │
 │                              │  of qubits.                                  │
 ├──────────────────────────────┴───────────────────────────────────────────────┤
 │ ENTER detail · / search · c compare · C compare view · f filter · ? help   │
 └──────────────────────────────────────────────────────────────────────────────┘
```

### Screens

| Screen | Description |
|--------|-------------|
| **SPLASH** | Animated boot sequence with loading bar |
| **BROWSE** | Main explorer — scrollable code list with live preview |
| **DETAIL** | Full-page view of a single code with all properties |
| **SEARCH** | Real-time substring filter overlay on BROWSE |
| **COMPARE** | Side-by-side comparison of 2-3 codes with winner metrics |
| **DESCRIBE** | Plain-language explanations of every code field |
| **HELP** | Complete keyboard reference |

### Keyboard Shortcuts

| Key | BROWSE | DETAIL | SEARCH | COMPARE |
|-----|--------|--------|--------|---------|
| `↑`/`k` | Move up | — | — | — |
| `↓`/`j` | Move down | — | — | — |
| `Enter` | Open detail | — | Select first result | — |
| `/` | Enter search | — | — | — |
| `c` | Stage for compare | Stage for compare | — | Clear selection |
| `C` | Open compare | — | — | — |
| `d` | Describe fields | Describe fields | — | — |
| `f` | Cycle family filter | — | — | — |
| `e` | — | Export JSON | — | — |
| `b`/`Esc` | Clear filters | Back to browse | Cancel search | Back to browse |
| `?` | Help | — | — | — |
| `q` | Quit | — | — | — |

See the full [Terminal UI Guide](docs/terminal-ui.md) for details.

## CLI

QLEX also provides a scriptable CLI for use in pipelines and automation. All output is clean plain text — no TUI rendering.

```bash
# List all codes
$ qlex list
  bacon-shor                Bacon-Shor Code
  color                     Color Code
  gross-144-12-12           Gross [[144,12,12]] qLDPC Code
  repetition                Repetition Code
  rotated-surface           Rotated Surface Code
  shor                      Shor [[9,1,3]] Code
  steane                    Steane [[7,1,3]] Code
  surface                   Surface Code
  toric                     Toric Code

# Get a specific code
$ qlex get surface

# Search
$ qlex search biased

# Compare codes
$ qlex compare surface color steane

# Export for downstream tools
$ qlex export surface

# Filter (flags are combinable)
$ qlex filter --family topological
$ qlex filter --hardware trapped_ion --fault-tolerant
$ qlex filter --tag CSS --tag stabilizer

# Version
$ qlex version
QLEX 0.1.0
by Qorex
```

See the full [CLI Reference](docs/cli-reference.md) for all options.

## Registry

QLEX ships with 9 QEC codes sourced from published literature. Every threshold value has a citation.

| Code | Family | [[n, k, d]] | Circuit Threshold | Depolarizing Threshold |
|------|--------|-------------|-------------------|----------------------|
| Surface Code | topological | [[2d²-1, 1, d]] | 0.0057 | 0.189 |
| Rotated Surface Code | topological | [[d², 1, d]] | 0.0057 | 0.189 |
| Toric Code | topological | [[2d², 2, d]] | 0.0075 | 0.189 |
| Color Code | topological | [[18, 1, 5]] | 0.0046 | 0.109 |
| Steane [[7,1,3]] | CSS | [[7, 1, 3]] | 0.00027 | — |
| Shor [[9,1,3]] | stabilizer | [[9, 1, 3]] | — | — |
| Bacon-Shor | subsystem | [[m×m, 1, d]] | 0.00042 | — |
| Repetition Code | stabilizer | [[n, 1, d]] | 0.0029 | — |
| Gross [[144,12,12]] | qLDPC | [[144, 12, 12]] | — | — |

See the [Registry Guide](docs/registry.md) for detailed information about each code, including hardware compatibility, supported decoders, and key papers.

## Ecosystem

<p align="center">
  <img src="assets/logos/QOREX.svg" alt="Qorex" width="200" />
</p>

QLEX is the foundational layer in the Qorex quantum computing infrastructure stack.

```
  ┌─────────────────────────────────────────────────────┐
  │         Future Qorex tools                          │
  │   (simulator · benchmarker · paper tracker)         │
  └────────────────────┬────────────────────────────────┘
                       │  imports
  ┌────────────────────▼────────────────────────────────┐
  │                   QLEX                              │
  │      QEC code registry & intelligence layer         │
  │              pip install qlex                       │
  └─────────────────────────────────────────────────────┘
```

Downstream tools consume QLEX's export configs to standardize how QEC code properties are passed between systems. The `to_export_config()` method produces a versioned dict that any Qorex tool can ingest:

```python
config = qlex.get("surface").to_export_config()
# Pass config["recommended_decoders"] to a decoder benchmarker
# Pass config["parameters"] to a circuit simulator
# Pass config["supported_noise_models"] to a noise characterizer
```

## Project Structure

```
qlex/
├── qlex/
│   ├── __init__.py          # Public API surface
│   ├── registry.py          # Core registry: load, query, filter
│   ├── models.py            # Pydantic v2 data models
│   ├── filters.py           # Filter and search logic
│   ├── compare.py           # Side-by-side code comparison
│   ├── export.py            # Export helpers for downstream Qorex tools
│   ├── exceptions.py        # All custom exceptions
│   ├── cli.py               # CLI entry point (argparse)
│   ├── ui/
│   │   ├── app.py           # Main TUI entry point
│   │   ├── renderer.py      # ASCII rendering primitives
│   │   ├── screens.py       # Screen render functions
│   │   ├── state.py         # UI state machine
│   │   └── theme.py         # Colors, glyphs, animations
│   └── data/
│       └── codes.json       # The full code registry
├── tests/                   # pytest test suite
├── docs/                    # Documentation
└── assets/
    └── logos/               # QLEX and Qorex brand assets
```

## Development

```bash
# Clone and install in dev mode
git clone https://github.com/qorex/qlex.git
cd qlex
pip install -e ".[dev]"

# Run tests
pytest -v

# Launch the TUI
qlex
```

## Contributing

To add a new QEC code, submit a PR that adds an entry to `qlex/data/codes.json`. Each entry must include all required fields — see the [Registry Guide](docs/registry.md) for the full schema. Threshold values must be sourced from published literature with appropriate citations in the `key_papers` field.

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for full guidelines.

## License

MIT — [Qorex](https://github.com/qorex)
