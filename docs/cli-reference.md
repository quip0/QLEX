<p align="center">
  <img src="../assets/logos/qlex.svg" alt="QLEX" width="320" />
</p>

# CLI Reference

QLEX provides a command-line interface for scripting, piping, and automation. All output is clean plain text — no TUI rendering, no curses.

---

## Usage

```
qlex [command] [options]
```

Running `qlex` with no arguments launches the [Terminal UI](terminal-ui.md).

---

## Commands

### `qlex list`

Print all codes in the registry, sorted alphabetically.

```bash
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
```

---

### `qlex get <id>`

Print the full summary of a code.

```bash
$ qlex get surface
============================================================
  Surface Code
  Family: topological
  Parameters: [[2d^2 - 1, 1, variable]]
────────────────────────────────────────────────────────────
  Thresholds:  depolarizing=0.1890  circuit_level=0.0057
  Hardware: superconducting, trapped_ion, neutral_atom, NV_center, silicon_spin
  Decoders: MWPM, Union-Find, Belief Propagation, Neural Network
  ...
============================================================
```

If the ID doesn't exist, the error message lists all valid IDs.

---

### `qlex search <query>`

Search for codes by substring (case-insensitive). Matches against name, description, tags, and noise models.

```bash
$ qlex search surface
  rotated-surface           Rotated Surface Code
  surface                   Surface Code
  toric                     Toric Code

$ qlex search biased
  bacon-shor                Bacon-Shor Code
  repetition                Repetition Code
  surface                   Surface Code
  toric                     Toric Code
```

---

### `qlex compare <id> <id> [id]`

Print a side-by-side comparison table for 2 or 3 codes.

```bash
$ qlex compare surface color steane
──────────────────────────────────────────────────────────────────────────
Property              surface                  color                    steane
──────────────────────────────────────────────────────────────────────────
Name                  Surface Code             Color Code               Steane [[7,1,3]] Code
Family                topological              topological              CSS
...
──────────────────────────────────────────────────────────────────────────
Winner (circuit_level_threshold)██ BEST
Winner (depolarizing_threshold) ██ BEST
Winner (qubit_efficiency)       ── no data
──────────────────────────────────────────────────────────────────────────
```

---

### `qlex export <id>`

Print the export config for a code as JSON. This is the format consumed by downstream Qorex tools.

```bash
$ qlex export surface
{
  "code_id": "surface",
  "code_name": "Surface Code",
  "parameters": {
    "n": "2d^2 - 1",
    "k": 1,
    "d": "variable"
  },
  "supported_noise_models": [
    "depolarizing",
    "biased",
    "erasure",
    "circuit_level",
    "amplitude_damping"
  ],
  "recommended_decoders": [
    "MWPM",
    "Union-Find",
    "Belief Propagation",
    "Neural Network"
  ],
  "threshold_reference": {
    "depolarizing": 0.189,
    "circuit_level": 0.0057,
    "notes": "Depolarizing threshold from Dennis et al. (2002)..."
  },
  "qlex_version": "0.1.0"
}
```

Pipe it into `jq` for further processing:

```bash
$ qlex export surface | jq '.recommended_decoders'
```

---

### `qlex filter [options]`

Filter codes by one or more criteria. All flags are optional and combinable.

| Flag | Type | Description |
|------|------|-------------|
| `--family <name>` | string | Filter by code family (e.g., `topological`, `CSS`) |
| `--hardware <platform>` | string | Filter by hardware compatibility |
| `--min-threshold <float>` | float | Minimum circuit-level threshold (excludes null) |
| `--fault-tolerant` | flag | Only fault-tolerant codes |
| `--tag <tag>` | string (repeatable) | Filter by tag — AND logic when repeated |

```bash
# Single filter
$ qlex filter --family topological
  color                     Color Code
  rotated-surface           Rotated Surface Code
  surface                   Surface Code
  toric                     Toric Code

# Combined filters
$ qlex filter --hardware trapped_ion --fault-tolerant
  bacon-shor                Bacon-Shor Code
  color                     Color Code
  ...

# Multiple tags (AND logic — code must have both)
$ qlex filter --tag CSS --tag stabilizer
  color                     Color Code
  gross-144-12-12           Gross [[144,12,12]] qLDPC Code
  ...
```

---

### `qlex version`

Print the version and brand line.

```bash
$ qlex version
QLEX 0.1.0
by Qorex
```

---

## Piping and Scripting

The CLI is designed for composition. All output is plain text that can be piped, grepped, or parsed.

```bash
# Count topological codes
qlex filter --family topological | wc -l

# Get all code IDs
qlex list | awk '{print $1}'

# Export all fault-tolerant codes as JSON
for id in $(qlex filter --fault-tolerant | awk '{print $1}'); do
  qlex export "$id"
done

# Search and get detail
qlex search surface | head -1 | awk '{print $1}' | xargs qlex get
```

---

<p align="center">
  <img src="../assets/logos/icon.svg" alt="QLEX" width="48" />
  <br />
  <sub>QLEX is a product of <a href="https://github.com/qorex">Qorex</a></sub>
</p>
