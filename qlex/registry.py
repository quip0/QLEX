"""Core registry: load, query, and filter QEC codes."""

from __future__ import annotations

import json
from pathlib import Path

from qlex.compare import Comparison
from qlex.exceptions import CodeNotFoundError, RegistryError
from qlex.filters import filter_codes
from qlex.models import QECCode


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
        """Case-insensitive substring search across name, description, and tags."""
        q = query.lower()
        results = []
        for code in self.list_codes():
            if q in code.name.lower():
                results.append(code)
                continue
            if q in code.description.lower():
                results.append(code)
                continue
            if any(q in tag.lower() for tag in code.tags):
                results.append(code)
                continue
            if any(q in nm.lower() for nm in code.noise_models):
                results.append(code)
                continue
        return results

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
