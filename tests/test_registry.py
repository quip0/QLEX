"""Tests for the QLEX registry."""

import pytest

import qlex
from qlex.exceptions import CodeNotFoundError
from qlex.models import QECCode


def test_get_surface_returns_correct_code() -> None:
    code = qlex.get("surface")
    assert isinstance(code, QECCode)
    assert code.name == "Surface Code"


def test_get_nonexistent_raises_code_not_found() -> None:
    with pytest.raises(CodeNotFoundError) as exc_info:
        qlex.get("nonexistent")
    assert "nonexistent" in str(exc_info.value)
    assert "surface" in str(exc_info.value)


def test_list_codes_returns_sorted_and_complete() -> None:
    codes = qlex.list_codes()
    assert len(codes) >= 8
    names = [c.name for c in codes]
    assert names == sorted(names, key=str.lower)


def test_search_surface_returns_at_least_two() -> None:
    results = qlex.search("surface")
    assert len(results) >= 2


def test_search_biased_returns_relevant_codes() -> None:
    results = qlex.search("biased")
    assert len(results) > 0
    for code in results:
        text = (
            code.description.lower()
            + " ".join(code.tags).lower()
            + " ".join(code.noise_models).lower()
        )
        assert "biased" in text


def test_search_nonsense_returns_empty() -> None:
    results = qlex.search("zzzzz")
    assert results == []


def test_count_returns_correct_integer() -> None:
    count = qlex.count()
    assert isinstance(count, int)
    assert count >= 8
    assert count == len(qlex.list_codes())


def test_families_returns_sorted_unique_list() -> None:
    families = qlex.families()
    assert len(families) > 0
    assert families == sorted(set(families))
    # No duplicates
    assert len(families) == len(set(families))
