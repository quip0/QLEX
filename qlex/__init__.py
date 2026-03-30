"""QLEX — The Quantum Lexicon. QEC code registry by Qorex."""

from __future__ import annotations

from typing import TYPE_CHECKING

from qlex.registry import Registry

if TYPE_CHECKING:
    from qlex.compare import Comparison
    from qlex.models import QECCode

__version__ = "0.1.0"

registry = Registry()


def get(code_id: str) -> QECCode:
    """Return a QEC code by its ID."""
    return registry.get(code_id)


def list_codes() -> list[QECCode]:
    """Return all codes sorted alphabetically by name."""
    return registry.list_codes()


def filter(**kwargs: object) -> list[QECCode]:
    """Filter codes by the given criteria."""
    return registry.filter(**kwargs)


def search(query: str) -> list[QECCode]:
    """Case-insensitive substring search across name, description, and tags."""
    return registry.search(query)


def compare(*ids: str) -> Comparison:
    """Compare two or more codes by ID."""
    return registry.compare(*ids)


def count() -> int:
    """Return the number of codes in the registry."""
    return registry.count()


def families() -> list[str]:
    """Return a unique sorted list of all code families."""
    return registry.families()
