"""Filter and search logic for QEC codes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from qlex.exceptions import FilterError

if TYPE_CHECKING:
    from qlex.models import QECCode

VALID_KWARGS = {
    "family",
    "hardware",
    "min_threshold",
    "fault_tolerant",
    "tags",
    "has_decoder",
    "magic_state_distillation",
}


def filter_codes(codes: list[QECCode], **kwargs: object) -> list[QECCode]:
    """Filter a list of QEC codes by the given criteria.

    All parameters are optional. Omitting a parameter applies no filter on that
    dimension. Unknown keyword arguments raise FilterError.
    """
    unknown = set(kwargs.keys()) - VALID_KWARGS
    if unknown:
        raise FilterError(
            f"Unknown filter parameter(s): {', '.join(sorted(unknown))}. "
            f"Valid parameters: {', '.join(sorted(VALID_KWARGS))}"
        )

    result = list(codes)

    if "family" in kwargs:
        family = kwargs["family"]
        result = [c for c in result if c.family == family]

    if "hardware" in kwargs:
        hw = kwargs["hardware"]
        result = [c for c in result if hw in c.hardware_compatibility]

    if "min_threshold" in kwargs:
        min_t = float(kwargs["min_threshold"])  # type: ignore[arg-type]
        result = [
            c for c in result
            if c.threshold.circuit_level is not None and c.threshold.circuit_level >= min_t
        ]

    if "fault_tolerant" in kwargs:
        ft = kwargs["fault_tolerant"]
        result = [c for c in result if c.fault_tolerant == ft]

    if "tags" in kwargs:
        required_tags: list[str] = kwargs["tags"]  # type: ignore[assignment]
        result = [
            c for c in result
            if all(tag in c.tags for tag in required_tags)
        ]

    if "has_decoder" in kwargs:
        decoder = kwargs["has_decoder"]
        result = [c for c in result if decoder in c.decoders]

    if "magic_state_distillation" in kwargs:
        msd = kwargs["magic_state_distillation"]
        result = [c for c in result if c.magic_state_distillation == msd]

    return result
