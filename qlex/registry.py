"""Core registry: load, query, and filter QEC codes."""

from __future__ import annotations

import json
from pathlib import Path

from qlex.compare import Comparison
from qlex.exceptions import CodeNotFoundError, RegistryError
from qlex.filters import filter_codes
from qlex.models import QECCode


def _score_code(code: QECCode, tokens: list[str], full_query: str) -> int:
    """Score a code against search tokens.  Return 0 if any token has no match."""
    total = 0
    for token in tokens:
        best = 0
        # High-value: ID and name
        if token in code.id:
            best = max(best, 100)
        if token in code.name.lower():
            best = max(best, 90)
        # Medium-high: family, tags
        if token in code.family.lower():
            best = max(best, 70)
        if any(token in t.lower() for t in code.tags):
            best = max(best, 60)
        # Medium: decoders, hardware, noise models, logical gates
        if any(token in d.lower() for d in code.decoders):
            best = max(best, 50)
        if any(token in hw.lower() for hw in code.hardware_compatibility):
            best = max(best, 50)
        if any(token in nm.lower() for nm in code.noise_models):
            best = max(best, 50)
        if any(token in g.lower() for g in code.logical_gates):
            best = max(best, 40)
        # Lower: connectivity, description, papers
        if token in code.connectivity.lower():
            best = max(best, 30)
        for paper in code.key_papers:
            if token in paper.title.lower():
                best = max(best, 35)
            if any(token in a.lower() for a in paper.authors):
                best = max(best, 35)
        if token in code.description.lower():
            best = max(best, 20)
        if best == 0:
            return 0  # every token must match somewhere
        total += best
    # Bonus for exact name/ID match
    if full_query == code.name.lower() or full_query == code.id:
        total += 200
    return total


class Registry:
    """In-memory QEC code registry loaded from codes.json at init time."""

    def __init__(self) -> None:
        self._codes: dict[str, QECCode] = {}
        self._load()

    def _load(self) -> None:
        """Load codes.json into memory. Called once at instantiation."""
        data_path = Path(__file__).parent / "data" / "codes.json"
        try:
            raw = data_path.read_text(encoding="utf-8")
            entries = json.loads(raw)
        except FileNotFoundError:
            raise RegistryError(f"Data file not found: {data_path}")
        except json.JSONDecodeError as e:
            raise RegistryError(f"Invalid JSON in {data_path}: {e}")

        for entry in entries:
            try:
                code = QECCode.model_validate(entry)
                self._codes[code.id] = code
            except Exception as e:
                raise RegistryError(f"Failed to parse code entry: {e}")

    def get(self, code_id: str) -> QECCode:
        """Return a QECCode by its ID, or raise CodeNotFoundError."""
        if code_id in self._codes:
            return self._codes[code_id]
        raise CodeNotFoundError(code_id, list(self._codes.keys()))

    def list_codes(self) -> list[QECCode]:
        """Return all codes sorted alphabetically by name."""
        return sorted(self._codes.values(), key=lambda c: c.name.lower())

    def filter(self, **kwargs: object) -> list[QECCode]:
        """Filter codes by the given criteria. Delegates to filters.py."""
        return filter_codes(self.list_codes(), **kwargs)

    def search(self, query: str) -> list[QECCode]:
        """Ranked multi-token search across all code fields.

        Splits the query into tokens and requires every token to match
        somewhere.  Results are ranked by *where* tokens match — name and
        ID hits score highest, description hits score lowest.
        """
        q = query.lower().strip()
        if not q:
            return self.list_codes()

        tokens = q.split()
        scored: list[tuple[int, QECCode]] = []

        for code in self.list_codes():
            score = _score_code(code, tokens, q)
            if score > 0:
                scored.append((score, code))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [code for _, code in scored]

    def compare(self, *ids: str) -> Comparison:
        """Compare two or more codes by ID. Delegates to compare.py."""
        codes = [self.get(code_id) for code_id in ids]
        return Comparison(codes)

    def count(self) -> int:
        """Return the number of codes in the registry."""
        return len(self._codes)

    def families(self) -> list[str]:
        """Return a unique sorted list of all code families."""
        return sorted(set(c.family for c in self._codes.values()))
