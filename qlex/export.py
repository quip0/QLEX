"""Export helpers for downstream Qorex tools."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qlex.models import QECCode


def to_export_config(code: QECCode) -> dict:
    """Return a dict formatted for downstream Qorex tool consumption."""
    from qlex import __version__

    return {
        "code_id": code.id,
        "code_name": code.name,
        "parameters": code.parameters.model_dump(),
        "supported_noise_models": list(code.noise_models),
        "recommended_decoders": list(code.decoders),
        "threshold_reference": code.threshold.model_dump(),
        "qlex_version": __version__,
    }


def validate_exportable(code: QECCode) -> bool:
    """Return True if the code has at least one noise model set."""
    return len(code.noise_models) > 0


def batch_export(codes: list[QECCode]) -> list[dict]:
    """Export a list of codes as export configs."""
    return [to_export_config(c) for c in codes]


def to_json(codes: list[QECCode]) -> str:
    """Serialize a list of codes to a JSON string."""
    return json.dumps([c.to_dict() for c in codes], indent=2, default=str)
