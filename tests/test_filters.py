"""Tests for the QLEX filter system."""

import pytest

import qlex
from qlex.exceptions import FilterError


def test_filter_by_family_topological() -> None:
    results = qlex.filter(family="topological")
    assert len(results) > 0
    for code in results:
        assert code.family == "topological"


def test_filter_by_hardware_trapped_ion() -> None:
    results = qlex.filter(hardware="trapped_ion")
    assert len(results) > 0
    for code in results:
        assert "trapped_ion" in code.hardware_compatibility


def test_filter_by_min_threshold_excludes_nulls() -> None:
    results = qlex.filter(min_threshold=0.005)
    assert len(results) > 0
    for code in results:
        assert code.threshold.circuit_level is not None
        assert code.threshold.circuit_level >= 0.005


def test_filter_fault_tolerant_true() -> None:
    results = qlex.filter(fault_tolerant=True)
    assert len(results) > 0
    for code in results:
        assert code.fault_tolerant is True


def test_filter_by_tags_and_logic() -> None:
    results = qlex.filter(tags=["CSS", "stabilizer"])
    assert len(results) > 0
    for code in results:
        assert "CSS" in code.tags
        assert "stabilizer" in code.tags


def test_filter_by_has_decoder_mwpm() -> None:
    results = qlex.filter(has_decoder="MWPM")
    assert len(results) > 0
    for code in results:
        assert "MWPM" in code.decoders


def test_combined_filters() -> None:
    results = qlex.filter(family="topological", fault_tolerant=True)
    assert len(results) > 0
    for code in results:
        assert code.family == "topological"
        assert code.fault_tolerant is True


def test_unknown_kwarg_raises_filter_error() -> None:
    with pytest.raises(FilterError):
        qlex.filter(nonexistent_param="value")
