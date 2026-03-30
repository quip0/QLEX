"""Tests for the QLEX comparison system."""

import pytest

import qlex
from qlex.exceptions import ComparisonError


def test_compare_two_codes() -> None:
    comp = qlex.compare("surface", "color")
    assert len(comp.codes) == 2


def test_to_dict_contains_both_ids() -> None:
    comp = qlex.compare("surface", "color")
    d = comp.to_dict()
    assert "surface" in d
    assert "color" in d


def test_winner_circuit_level_threshold() -> None:
    comp = qlex.compare("surface", "color")
    winner = comp.winner("circuit_level_threshold")
    assert winner in ("surface", "color")


def test_compare_single_code_raises_error() -> None:
    with pytest.raises(ComparisonError):
        qlex.compare("surface")


def test_table_produces_output() -> None:
    comp = qlex.compare("surface", "color")
    table = comp.table()
    assert isinstance(table, str)
    assert len(table) > 0
    assert "surface" in table.lower() or "Surface" in table
