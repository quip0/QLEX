"""Tests for the QLEX export system."""

import json

import qlex
from qlex.export import batch_export, to_export_config, to_json, validate_exportable


def test_to_export_config_has_required_keys() -> None:
    code = qlex.get("surface")
    config = to_export_config(code)
    assert "code_id" in config
    assert "code_name" in config
    assert "parameters" in config
    assert "supported_noise_models" in config
    assert "recommended_decoders" in config
    assert "threshold_reference" in config
    assert "qlex_version" in config
    assert config["qlex_version"] == "0.1.0"


def test_validate_exportable_surface() -> None:
    code = qlex.get("surface")
    assert validate_exportable(code) is True


def test_batch_export_returns_correct_length() -> None:
    surface = qlex.get("surface")
    color = qlex.get("color")
    result = batch_export([surface, color])
    assert len(result) == 2
    assert result[0]["code_id"] == "surface"
    assert result[1]["code_id"] == "color"


def test_to_json_returns_valid_json() -> None:
    surface = qlex.get("surface")
    result = to_json([surface])
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 1
    assert parsed[0]["id"] == "surface"
