<p align="center">
  <img src="../assets/logos/icon.svg" alt="QLEX" width="64" />
</p>

# Contributing to QLEX

Thank you for your interest in contributing to QLEX! This guide covers how to add new QEC codes, fix bugs, and improve the project.

---

## Adding a New QEC Code

This is the most common contribution. To add a new code:

1. **Fork and clone** the repository
2. **Edit `qlex/data/codes.json`** — add a new entry with all required fields (see the [Registry Guide](registry.md) for the full schema)
3. **Verify your data**:
   - All threshold values must come from published papers
   - Add the source papers to `key_papers` with arXiv IDs
   - Use `null` (not `0`) for unknown threshold values
   - Ensure `tags` are descriptive and consistent with existing codes
4. **Run the tests** to make sure nothing breaks:
   ```bash
   pip install -e ".[dev]"
   pytest -v
   ```
5. **Submit a PR** with a clear title like `"Add [[n,k,d]] Code Name"`

### Example Entry

```json
{
  "id": "my-new-code",
  "name": "My New [[n,k,d]] Code",
  "family": "stabilizer",
  "parameters": { "n": 15, "k": 1, "d": 3 },
  "threshold": {
    "depolarizing": null,
    "circuit_level": 0.001,
    "notes": "From Author et al. (2024) under standard circuit noise."
  },
  "hardware_compatibility": ["superconducting", "trapped_ion"],
  "connectivity": "Description of required qubit layout",
  "decoders": ["Decoder Name"],
  "noise_models": ["depolarizing", "circuit_level"],
  "fault_tolerant": true,
  "logical_gates": ["CNOT", "H"],
  "magic_state_distillation": false,
  "key_papers": [
    {
      "title": "Paper Title",
      "authors": ["First Author", "Second Author"],
      "year": 2024,
      "arxiv": "2401.00000"
    }
  ],
  "description": "Two to four sentences describing the code technically.",
  "tags": ["stabilizer", "relevant-tag"]
}
```

---

## Development Setup

```bash
git clone https://github.com/qorex/qlex.git
cd qlex
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest -v                   # all tests
pytest tests/test_registry.py  # specific test file
pytest -v --tb=short        # shorter traceback
```

All tests use the real `codes.json` — no mocking of the registry.

### Launching the TUI

```bash
qlex                        # via console script
python -m qlex.ui.app       # via module
```

---

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
│   ├── exceptions.py        # Custom exceptions
│   ├── cli.py               # CLI entry point
│   ├── ui/                  # Terminal UI (curses)
│   └── data/
│       └── codes.json       # The code registry
├── tests/                   # pytest suite
├── docs/                    # Documentation
└── assets/logos/            # Brand assets
```

---

## Code Style

- Type hints on every function signature
- Docstrings on all public functions and classes
- No runtime dependencies beyond Pydantic + stdlib
- The TUI uses only `curses` (stdlib) — no external TUI frameworks

---

## Bug Reports

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Python version and OS

---

## Code of Conduct

Be respectful, constructive, and collaborative. QLEX is built for the quantum computing research community — let's keep it welcoming.

---

<p align="center">
  <sub>QLEX is a product of <a href="https://github.com/qorex">Qorex</a></sub>
</p>
