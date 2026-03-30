"""Side-by-side QEC code comparison."""

from __future__ import annotations

from typing import TYPE_CHECKING

from qlex.exceptions import ComparisonError

if TYPE_CHECKING:
    from qlex.models import QECCode


class Comparison:
    """Side-by-side comparison of two or more QEC codes."""

    def __init__(self, codes: list[QECCode]) -> None:
        if len(codes) < 2:
            raise ComparisonError("At least 2 codes are required for comparison")
        self.codes = codes

    def table(self) -> str:
        """Return a clean ASCII comparison table."""
        col_width = 25
        label_width = 22

        ids = [c.id for c in self.codes]
        header = f"{'Property':<{label_width}}" + "".join(f"{cid:<{col_width}}" for cid in ids)
        sep = "─" * (label_width + col_width * len(self.codes))

        rows = [sep, header, sep]

        def _row(label: str, values: list[str]) -> str:
            return f"{label:<{label_width}}" + "".join(f"{v:<{col_width}}" for v in values)

        rows.append(_row("Name", [c.name for c in self.codes]))
        rows.append(_row("Family", [c.family for c in self.codes]))
        rows.append(_row("n", [str(c.parameters.n) for c in self.codes]))
        rows.append(_row("k", [str(c.parameters.k) for c in self.codes]))
        rows.append(_row("d", [str(c.parameters.d) for c in self.codes]))

        rows.append(_row(
            "Circuit threshold",
            [f"{c.threshold.circuit_level:.4f}" if c.threshold.circuit_level is not None else "N/A"
             for c in self.codes],
        ))
        rows.append(_row(
            "Depol. threshold",
            [f"{c.threshold.depolarizing:.4f}" if c.threshold.depolarizing is not None else "N/A"
             for c in self.codes],
        ))
        rows.append(_row(
            "Fault tolerant",
            ["Yes" if c.fault_tolerant else "No" for c in self.codes],
        ))
        rows.append(_row(
            "Magic state dist.",
            ["Yes" if c.magic_state_distillation else "No" for c in self.codes],
        ))
        rows.append(_row(
            "Hardware",
            [", ".join(c.hardware_compatibility[:3]) for c in self.codes],
        ))
        rows.append(_row(
            "Decoders",
            [", ".join(c.decoders[:3]) for c in self.codes],
        ))

        rows.append(sep)

        # Winner rows
        for metric in ("circuit_level_threshold", "depolarizing_threshold", "qubit_efficiency"):
            try:
                w = self.winner(metric)
                rows.append(_row(f"Winner ({metric})", [
                    "██ BEST" if c.id == w else "" for c in self.codes
                ]))
            except ComparisonError:
                rows.append(_row(f"Winner ({metric})", ["── no data"] * len(self.codes)))

        rows.append(sep)
        return "\n".join(rows)

    def to_dict(self) -> dict:
        """Return structured dict keyed by code ID with all comparable properties."""
        result = {}
        for code in self.codes:
            result[code.id] = {
                "name": code.name,
                "family": code.family,
                "parameters": code.parameters.model_dump(),
                "threshold": code.threshold.model_dump(),
                "fault_tolerant": code.fault_tolerant,
                "magic_state_distillation": code.magic_state_distillation,
                "hardware_compatibility": code.hardware_compatibility,
                "decoders": code.decoders,
                "noise_models": code.noise_models,
                "logical_gates": code.logical_gates,
            }
        return result

    def winner(self, metric: str) -> str:
        """Return code ID with best value for the given metric.

        Supported metrics:
        - circuit_level_threshold: higher is better
        - depolarizing_threshold: higher is better
        - qubit_efficiency: k/n ratio, higher is better (skips non-numeric n)
        """
        if metric == "circuit_level_threshold":
            candidates = [
                (c.id, c.threshold.circuit_level)
                for c in self.codes
                if c.threshold.circuit_level is not None
            ]
            if not candidates:
                raise ComparisonError(
                    "Cannot determine winner for circuit_level_threshold: all values are null"
                )
            return max(candidates, key=lambda x: x[1])[0]

        elif metric == "depolarizing_threshold":
            candidates = [
                (c.id, c.threshold.depolarizing)
                for c in self.codes
                if c.threshold.depolarizing is not None
            ]
            if not candidates:
                raise ComparisonError(
                    "Cannot determine winner for depolarizing_threshold: all values are null"
                )
            return max(candidates, key=lambda x: x[1])[0]

        elif metric == "qubit_efficiency":
            candidates = []
            for c in self.codes:
                if isinstance(c.parameters.n, int) and c.parameters.n > 0:
                    candidates.append((c.id, c.parameters.k / c.parameters.n))
            if not candidates:
                raise ComparisonError(
                    "Cannot determine winner for qubit_efficiency: no codes with numeric n"
                )
            return max(candidates, key=lambda x: x[1])[0]

        else:
            raise ComparisonError(f"Unknown metric: {metric}")
