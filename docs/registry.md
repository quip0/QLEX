<p align="center">
  <img src="../assets/logos/qlex.svg" alt="QLEX" width="320" />
</p>

# Registry Guide

QLEX ships with a curated registry of quantum error-correcting codes. Every entry is sourced from published QEC literature, and all threshold values have citations.

---

## Data Source

All code data lives in a single file: [`qlex/data/codes.json`](../qlex/data/codes.json). The registry is loaded into memory once at import time and never re-read from disk.

---

## Codes

### Surface Code

| Property | Value |
|----------|-------|
| **ID** | `surface` |
| **Family** | topological |
| **Parameters** | [[2d²-1, 1, variable]] |
| **Circuit-level threshold** | 0.0057 |
| **Depolarizing threshold** | 0.189 |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom, NV_center, silicon_spin |
| **Decoders** | MWPM, Union-Find, Belief Propagation, Neural Network |
| **Connectivity** | 2D nearest-neighbor grid with periodic or open boundaries |

The surface code is a topological stabilizer code defined on a 2D lattice of qubits. It achieves high error thresholds due to local stabilizer checks and is a leading candidate for fault-tolerant quantum computing with superconducting architectures. The code encodes one logical qubit per planar patch and supports transversal CNOT via lattice surgery.

**Key papers:**
- Dennis, Kitaev, Landahl, Preskill (2002) — *Topological quantum memory* — `quant-ph/0110143`
- Kitaev (2003) — *Fault-tolerant quantum computation by anyons* — `quant-ph/9707021`

---

### Rotated Surface Code

| Property | Value |
|----------|-------|
| **ID** | `rotated-surface` |
| **Family** | topological |
| **Parameters** | [[d², 1, variable]] |
| **Circuit-level threshold** | 0.0057 |
| **Depolarizing threshold** | 0.189 |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom, silicon_spin |
| **Decoders** | MWPM, Union-Find, Belief Propagation |
| **Connectivity** | 2D nearest-neighbor grid, rotated 45 degrees |

A more qubit-efficient variant of the standard surface code, requiring only d² physical qubits instead of 2d²-1 for distance d. It achieves this by rotating the lattice by 45 degrees, placing data qubits at vertices of a tilted grid.

**Key papers:**
- Fowler, Mariantoni, Martinis, Cleland (2012) — *Surface codes: Towards practical large-scale quantum computation* — `1208.0928`

---

### Toric Code

| Property | Value |
|----------|-------|
| **ID** | `toric` |
| **Family** | topological |
| **Parameters** | [[2d², 2, variable]] |
| **Circuit-level threshold** | 0.0075 |
| **Depolarizing threshold** | 0.189 |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, neutral_atom |
| **Decoders** | MWPM, Union-Find, Renormalization Group |
| **Connectivity** | 2D nearest-neighbor grid with periodic boundary conditions (torus) |

The original topological quantum error-correcting code, defined on a torus. It encodes two logical qubits and has been foundational in establishing the connection between quantum error correction and topological order. The surface code is its planar variant with open boundaries.

**Key papers:**
- Dennis, Kitaev, Landahl, Preskill (2002) — *Topological quantum memory* — `quant-ph/0110143`
- Wang, Harrington, Preskill (2003) — *Confinement-Higgs transition in a disordered gauge theory...* — `quant-ph/0207088`

---

### Color Code

| Property | Value |
|----------|-------|
| **ID** | `color` |
| **Family** | topological |
| **Parameters** | [[18, 1, 5]] |
| **Circuit-level threshold** | 0.0046 |
| **Depolarizing threshold** | 0.109 |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom |
| **Decoders** | Restriction Decoder, Projection Decoder, MWPM |
| **Connectivity** | Trivalent lattice (4.8.8, 6.6.6, or 4.6.12 tilings) |

Color codes are topological stabilizer codes defined on trivalent lattices with 3-colorable faces. They support a transversal implementation of the full Clifford group, which is an advantage over surface codes.

**Key papers:**
- Bombin, Martin-Delgado (2006) — *Topological quantum distillation* — `quant-ph/0605138`
- Landahl, Anderson, Rice (2011) — *Fault-tolerant quantum computing with color codes* — `1108.5738`

---

### Steane [[7,1,3]] Code

| Property | Value |
|----------|-------|
| **ID** | `steane` |
| **Family** | CSS |
| **Parameters** | [[7, 1, 3]] |
| **Circuit-level threshold** | 0.00027 |
| **Depolarizing threshold** | — |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom, photonic, NV_center, silicon_spin |
| **Decoders** | Lookup Table, Steane Syndrome Decoder |
| **Connectivity** | All-to-all (7 qubits, dense stabilizer checks) |

The Steane code is the smallest CSS code, encoding one logical qubit into seven physical qubits with distance 3. Based on the classical [7,4,3] Hamming code, it supports the full transversal Clifford group.

**Key papers:**
- Steane (1996) — *Error correcting codes in quantum theory* — `quant-ph/9601029`

---

### Shor [[9,1,3]] Code

| Property | Value |
|----------|-------|
| **ID** | `shor` |
| **Family** | stabilizer |
| **Parameters** | [[9, 1, 3]] |
| **Circuit-level threshold** | — |
| **Depolarizing threshold** | — |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom, photonic, NV_center, silicon_spin |
| **Decoders** | Lookup Table, Majority Vote |
| **Connectivity** | Groups of 3 qubits in blocks of 3 (concatenated structure) |

The first quantum error-correcting code, encoding one logical qubit into nine physical qubits. It uses a concatenation of a 3-qubit bit-flip code and a 3-qubit phase-flip code. Foundational to the field and widely used in introductory QEC.

**Key papers:**
- Shor (1995) — *Scheme for reducing decoherence in quantum computer memory* — `quant-ph/9507018`

---

### Bacon-Shor Code

| Property | Value |
|----------|-------|
| **ID** | `bacon-shor` |
| **Family** | subsystem |
| **Parameters** | [[m×m, 1, variable]] |
| **Circuit-level threshold** | 0.00042 |
| **Depolarizing threshold** | — |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, trapped_ion, neutral_atom |
| **Decoders** | Majority Vote, Belief Propagation |
| **Connectivity** | 2D grid with row and column parity checks |

A subsystem code defined on an m×m grid. It uses gauge operators to simplify syndrome extraction, requiring only 2-qubit measurements instead of higher-weight stabilizer checks. Particularly well-suited for biased noise models.

**Key papers:**
- Bacon (2006) — *Operator quantum error-correcting subsystems for self-correcting quantum memories* — `quant-ph/0506023`
- Aliferis, Preskill (2008) — *Fault-tolerant quantum computation against biased noise* — `0710.1301`

---

### Repetition Code

| Property | Value |
|----------|-------|
| **ID** | `repetition` |
| **Family** | stabilizer |
| **Parameters** | [[variable, 1, variable]] |
| **Circuit-level threshold** | 0.0029 |
| **Depolarizing threshold** | — |
| **Fault tolerant** | No |
| **Hardware** | superconducting, trapped_ion, neutral_atom, NV_center, silicon_spin |
| **Decoders** | MWPM, Majority Vote |
| **Connectivity** | 1D nearest-neighbor chain |

The simplest quantum error-correcting code. It can only correct one type of Pauli error (bit-flip or phase-flip), making it a classical code in a quantum setting. Widely used for benchmarking hardware and decoders.

**Key papers:**
- Google Quantum AI (2023) — *Suppressing quantum errors by scaling a surface code logical qubit* — `2207.06431`

---

### Gross [[144,12,12]] qLDPC Code

| Property | Value |
|----------|-------|
| **ID** | `gross-144-12-12` |
| **Family** | qLDPC |
| **Parameters** | [[144, 12, 12]] |
| **Circuit-level threshold** | — |
| **Depolarizing threshold** | — |
| **Fault tolerant** | Yes |
| **Hardware** | superconducting, neutral_atom |
| **Decoders** | Belief Propagation + OSD, Small-Set Flip |
| **Connectivity** | Non-local; bivariate bicycle structure with weight-6 checks |

A bivariate bicycle quantum LDPC code that encodes 12 logical qubits into 144 physical qubits with distance 12. It achieves a high encoding rate (k/n = 1/12) compared to surface codes, marking a significant milestone for practical QEC.

**Key papers:**
- Bravyi, Cross, Gambetta, Maslov, Rall, Yoder (2024) — *Quantum error correction below the surface code threshold* — `2408.13687`
- Bravyi, Cross, Gambetta, Maslov, Rall, Yoder (2024) — *High-threshold and low-overhead fault-tolerant quantum memory* — `2308.07915`

---

## Code Entry Schema

Each code entry in `codes.json` must include these fields:

```
id                        string    lowercase, hyphen-separated
name                      string    full human-readable name
family                    string    topological | CSS | stabilizer | qLDPC | subsystem
parameters
  n                       int|str   number of physical qubits or formula
  k                       int       number of logical qubits
  d                       int|str   code distance or "variable"
threshold
  depolarizing            float|null
  circuit_level           float|null
  notes                   string    conditions and references
hardware_compatibility    [string]  superconducting | trapped_ion | neutral_atom |
                                    photonic | NV_center | silicon_spin
connectivity              string    qubit connectivity description
decoders                  [string]  decoder algorithm names
noise_models              [string]  depolarizing | biased | erasure | circuit_level |
                                    amplitude_damping
fault_tolerant            boolean
logical_gates             [string]  gate strings
magic_state_distillation  boolean
key_papers                [object]  title, authors [], year, arxiv
description               string    2-4 sentence technical description
tags                      [string]  descriptive tags
```

- All list fields must be present even if empty (`[]`)
- All null numeric fields must be explicitly `null`, not omitted
- Threshold values must be sourced from published literature

---

## Code Families

| Family | Description | Codes in registry |
|--------|-------------|-------------------|
| **topological** | Codes defined on lattices with topological protection | Surface, Rotated Surface, Toric, Color |
| **CSS** | Calderbank-Shor-Steane codes from classical code pairs | Steane |
| **stabilizer** | General stabilizer formalism codes | Shor, Repetition |
| **subsystem** | Codes with gauge operators for simplified syndrome extraction | Bacon-Shor |
| **qLDPC** | Quantum low-density parity-check codes | Gross [[144,12,12]] |

---

<p align="center">
  <img src="../assets/logos/icon.svg" alt="QLEX" width="48" />
  <br />
  <sub>QLEX is a product of <a href="https://github.com/qorex">Qorex</a></sub>
</p>
