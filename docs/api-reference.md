<p align="center">
  <img src="../assets/logos/qlex.svg" alt="QLEX" width="320" />
</p>

# API Reference

This document covers every public function and class in the QLEX Python API.

---

## Top-Level API

All of these are importable directly from `qlex`:

```python
import qlex

qlex.get(id)
qlex.list_codes()
qlex.filter(**kwargs)
qlex.search(query)
qlex.compare(*ids)
qlex.count()
qlex.families()
qlex.registry          # direct Registry instance
qlex.__version__       # "0.1.0"
```

---

### `qlex.get(code_id: str) -> QECCode`

Look up a QEC code by its unique ID.

```python
surface = qlex.get("surface")
print(surface.name)  # "Surface Code"
```

**Raises:** `CodeNotFoundError` if the ID doesn't exist. The error message includes all valid IDs.

```python
try:
    qlex.get("nonexistent")
except qlex.exceptions.CodeNotFoundError as e:
    print(e)
    # Code 'nonexistent' not found. Available IDs: bacon-shor, color, ...
```

---

### `qlex.list_codes() -> list[QECCode]`

Return all codes in the registry, sorted alphabetically by name.

```python
for code in qlex.list_codes():
    print(f"{code.id}: {code.name}")
```

---

### `qlex.filter(**kwargs) -> list[QECCode]`

Filter codes by one or more criteria. All parameters are optional and combinable. Omitting a parameter applies no filter on that dimension.

**Supported parameters:**

| Parameter | Type | Behavior |
|-----------|------|----------|
| `family` | `str` | Exact match on code family |
| `hardware` | `str` | Must appear in `hardware_compatibility` |
| `min_threshold` | `float` | Minimum `circuit_level` threshold; skips null |
| `fault_tolerant` | `bool` | Exact match |
| `tags` | `list[str]` | AND logic — code must have ALL listed tags |
| `has_decoder` | `str` | Must appear in `decoders` list |
| `magic_state_distillation` | `bool` | Exact match |

```python
# Single filter
topological = qlex.filter(family="topological")

# Combined filters
results = qlex.filter(
    fault_tolerant=True,
    hardware="superconducting",
    min_threshold=0.005,
)

# Tag intersection (AND logic)
css_stab = qlex.filter(tags=["CSS", "stabilizer"])
```

**Raises:** `FilterError` if an unknown keyword argument is passed.

---

### `qlex.search(query: str) -> list[QECCode]`

Case-insensitive substring search across a code's `name`, `description`, `tags`, and `noise_models`.

```python
results = qlex.search("surface")    # matches Surface Code, Rotated Surface Code
results = qlex.search("biased")     # matches codes with biased noise support
results = qlex.search("zzzzz")      # returns []
```

---

### `qlex.compare(*ids: str) -> Comparison`

Create a side-by-side comparison of two or more codes.

```python
comp = qlex.compare("surface", "color", "steane")
print(comp.table())

# Get the winner for a specific metric
winner = comp.winner("circuit_level_threshold")
print(winner)  # "surface"
```

**Raises:** `CodeNotFoundError` if any ID is invalid. `ComparisonError` if fewer than 2 IDs are provided.

---

### `qlex.count() -> int`

Return the total number of codes in the registry.

```python
print(qlex.count())  # 9
```

---

### `qlex.families() -> list[str]`

Return a sorted, deduplicated list of all code families in the registry.

```python
print(qlex.families())
# ['CSS', 'qLDPC', 'stabilizer', 'subsystem', 'topological']
```

---

## Data Models

All models use [Pydantic v2](https://docs.pydantic.dev/) and are importable from `qlex.models`.

### `QECCode`

The main data model representing a single quantum error-correcting code.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier (lowercase, hyphen-separated) |
| `name` | `str` | Full human-readable name |
| `family` | `str` | One of: `topological`, `CSS`, `stabilizer`, `qLDPC`, `subsystem` |
| `parameters` | `CodeParameters` | Code parameters [[n, k, d]] |
| `threshold` | `Threshold` | Error threshold values |
| `hardware_compatibility` | `list[str]` | Compatible hardware platforms |
| `connectivity` | `str` | Required qubit connectivity |
| `decoders` | `list[str]` | Compatible decoder algorithms |
| `noise_models` | `list[str]` | Supported noise models |
| `fault_tolerant` | `bool` | Whether the code supports fault tolerance |
| `logical_gates` | `list[str]` | Available logical gate operations |
| `magic_state_distillation` | `bool` | Whether MSD is supported |
| `key_papers` | `list[Paper]` | Key publications about this code |
| `description` | `str` | Technical description |
| `tags` | `list[str]` | Descriptive tags for filtering |

**Methods:**

#### `summary() -> str`

Return a formatted text card summarizing the code. Used by the TUI and CLI.

```python
surface = qlex.get("surface")
print(surface.summary())
# ============================================================
#   Surface Code
#   Family: topological
#   Parameters: [[2d^2 - 1, 1, variable]]
# ────────────────────────────────────────────────────────────
#   Thresholds:  depolarizing=0.1890  circuit_level=0.0057
#   ...
```

#### `to_dict() -> dict`

Return the raw dictionary representation (via Pydantic's `model_dump()`).

```python
d = surface.to_dict()
print(d["parameters"]["n"])  # "2d^2 - 1"
```

#### `to_export_config() -> dict`

Return a dict formatted for downstream Qorex tool consumption. Includes a `qlex_version` key for compatibility tracking.

```python
config = surface.to_export_config()
# {
#   "code_id": "surface",
#   "code_name": "Surface Code",
#   "parameters": {"n": "2d^2 - 1", "k": 1, "d": "variable"},
#   "supported_noise_models": [...],
#   "recommended_decoders": [...],
#   "threshold_reference": {...},
#   "qlex_version": "0.1.0"
# }
```

### `CodeParameters`

| Field | Type | Description |
|-------|------|-------------|
| `n` | `int \| str` | Number of physical qubits (integer or formula) |
| `k` | `int` | Number of logical qubits |
| `d` | `int \| str` | Code distance (integer or `"variable"`) |

### `Threshold`

| Field | Type | Description |
|-------|------|-------------|
| `depolarizing` | `float \| None` | Depolarizing noise threshold |
| `circuit_level` | `float \| None` | Circuit-level noise threshold |
| `notes` | `str` | Conditions and references |

### `Paper`

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Paper title |
| `authors` | `list[str]` | Author names |
| `year` | `int` | Publication year |
| `arxiv` | `str` | arXiv identifier |

---

## Comparison

Importable from `qlex.compare`.

### `Comparison`

Created by `qlex.compare()`. Requires at least 2 codes.

#### `Comparison.codes -> list[QECCode]`

The list of codes being compared.

#### `Comparison.table() -> str`

Return a formatted ASCII comparison table.

```python
comp = qlex.compare("surface", "color")
print(comp.table())
# ──────────────────────────────────────────────────────────
# Property              surface                  color
# ──────────────────────────────────────────────────────────
# Name                  Surface Code             Color Code
# Family                topological              topological
# ...
```

#### `Comparison.to_dict() -> dict`

Return a structured dict keyed by code ID with all comparable properties.

```python
d = comp.to_dict()
print(d["surface"]["threshold"]["circuit_level"])  # 0.0057
```

#### `Comparison.winner(metric: str) -> str`

Return the code ID with the best value for the given metric.

**Supported metrics:**

| Metric | Strategy | Notes |
|--------|----------|-------|
| `circuit_level_threshold` | Higher is better | Skips null values |
| `depolarizing_threshold` | Higher is better | Skips null values |
| `qubit_efficiency` | Higher k/n ratio | Skips non-numeric n |

```python
winner = comp.winner("circuit_level_threshold")
```

**Raises:** `ComparisonError` if no winner can be determined (e.g., all values are null).

---

## Export Utilities

Standalone functions importable from `qlex.export`. These work without importing the full registry.

### `to_export_config(code: QECCode) -> dict`

Same as `QECCode.to_export_config()` but as a standalone function.

### `validate_exportable(code: QECCode) -> bool`

Return `True` if the code has at least one noise model set.

```python
from qlex.export import validate_exportable
assert validate_exportable(qlex.get("surface")) is True
```

### `batch_export(codes: list[QECCode]) -> list[dict]`

Export multiple codes at once.

```python
from qlex.export import batch_export
configs = batch_export(qlex.list_codes())
```

### `to_json(codes: list[QECCode]) -> str`

Serialize a list of codes to a JSON string.

```python
from qlex.export import to_json
json_str = to_json(qlex.list_codes())
```

---

## Exceptions

All importable from `qlex.exceptions`.

| Exception | When it's raised |
|-----------|-----------------|
| `CodeNotFoundError(code_id, available_ids)` | `get()` with an invalid ID |
| `ComparisonError(message)` | `compare()` with < 2 codes, or `winner()` with no data |
| `FilterError(message)` | `filter()` with an unknown keyword argument |
| `RegistryError(message)` | `codes.json` is missing, corrupt, or contains invalid entries |

All exceptions produce human-readable messages including actionable context (e.g., `CodeNotFoundError` lists all valid IDs).

---

<p align="center">
  <img src="../assets/logos/icon.svg" alt="QLEX" width="48" />
  <br />
  <sub>QLEX is a product of <a href="https://github.com/qorex">Qorex</a></sub>
</p>
