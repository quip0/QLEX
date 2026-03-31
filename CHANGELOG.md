# CHANGELOG

## [0.1.1] — UI Enhancements

### Added
- **DESCRIBE screen** — press `d` from BROWSE or DETAIL to view plain-language explanations of every field in a QEC code entry (parameters, thresholds, hardware, connectivity, decoders, noise models, logical gates, key papers). Toggle back with `ESC` or `d`.
- **Sitting cat mascot** — an ASCII cat sits in the bottom-left corner of the screen with an animated tail wag (pendulum cycle: `\`, `|`, `/`, `|`). Appears on all screens except SPLASH.

- **36 new QEC codes** — registry expanded from 9 to 45 codes across 6 families: topological (17), qLDPC (9), CSS (7), stabilizer (5), subsystem (4), and bosonic (3). New entries include Floquet codes, asymptotically good qLDPC codes (Quantum Tanner, Lifted Product), bosonic codes (GKP, Cat, Binomial), and many more, each with real parameters, threshold values, and arXiv-linked key papers.

### Changed
- **Logo redesign** — replaced box-drawing characters (`╗`, `╔`, `║`) with clean solid-block (`█`) letterforms that match the QLEX SVG logo. Added a subtle drop shadow rendered with dim `░` characters offset +1 row/column.
- Footer hints updated to include the new `d describe` keybinding on BROWSE and DETAIL screens.

---

## [0.1.0] — Initial Release

### Added
- QLEX code registry with 9 QEC codes
- Python API: get, list, filter, search, compare, export
- Terminal UI: SPLASH, BROWSE, DETAIL, SEARCH, COMPARE, HELP screens
- CLI entry point with all subcommands
- Pydantic v2 data models
- Full pytest test suite
- Documentation: API reference, CLI reference, Terminal UI guide, Registry guide, Contributing guide

### Qorex
QLEX is the first product in the Qorex ecosystem.
