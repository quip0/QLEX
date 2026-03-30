"""Pydantic v2 data models for QLEX QEC code registry."""

from __future__ import annotations

from typing import Union

from pydantic import BaseModel, Field


class CodeParameters(BaseModel):
    """Physical parameters of a QEC code."""

    n: Union[int, str] = Field(description="Number of physical qubits (integer or formula string)")
    k: int = Field(description="Number of encoded logical qubits")
    d: Union[int, str] = Field(description="Code distance (integer or 'variable')")


class Threshold(BaseModel):
    """Error threshold values for a QEC code."""

    depolarizing: float | None = Field(default=None, description="Depolarizing noise threshold (fraction)")
    circuit_level: float | None = Field(default=None, description="Circuit-level noise threshold (fraction)")
    notes: str = Field(default="", description="Conditions and references for threshold values")


class Paper(BaseModel):
    """Reference to a key publication."""

    title: str = Field(description="Paper title")
    authors: list[str] = Field(default_factory=list, description="List of author names")
    year: int = Field(description="Publication year")
    arxiv: str = Field(description="arXiv identifier")


class QECCode(BaseModel):
    """Complete representation of a quantum error-correcting code."""

    id: str = Field(description="Unique identifier, lowercase hyphen-separated")
    name: str = Field(description="Full human-readable name")
    family: str = Field(description="Code family: topological, CSS, stabilizer, qLDPC, or subsystem")
    parameters: CodeParameters = Field(description="Code parameters [[n,k,d]]")
    threshold: Threshold = Field(description="Error thresholds")
    hardware_compatibility: list[str] = Field(default_factory=list, description="Compatible hardware platforms")
    connectivity: str = Field(default="", description="Required qubit connectivity")
    decoders: list[str] = Field(default_factory=list, description="Compatible decoder algorithms")
    noise_models: list[str] = Field(default_factory=list, description="Supported noise models")
    fault_tolerant: bool = Field(default=False, description="Whether the code supports fault-tolerant operations")
    logical_gates: list[str] = Field(default_factory=list, description="Available logical gate operations")
    magic_state_distillation: bool = Field(default=False, description="Whether magic state distillation is supported")
    key_papers: list[Paper] = Field(default_factory=list, description="Key publications about this code")
    description: str = Field(default="", description="Technical description of the code")
    tags: list[str] = Field(default_factory=list, description="Descriptive tags for filtering")

    def summary(self) -> str:
        """Return a formatted text card summarizing this code."""
        lines = []
        lines.append(f"{'=' * 60}")
        lines.append(f"  {self.name}")
        lines.append(f"  Family: {self.family}")
        lines.append(f"  Parameters: [[{self.parameters.n}, {self.parameters.k}, {self.parameters.d}]]")
        lines.append(f"{'─' * 60}")

        dep = f"{self.threshold.depolarizing:.4f}" if self.threshold.depolarizing is not None else "N/A"
        cir = f"{self.threshold.circuit_level:.4f}" if self.threshold.circuit_level is not None else "N/A"
        lines.append(f"  Thresholds:  depolarizing={dep}  circuit_level={cir}")

        if self.hardware_compatibility:
            lines.append(f"  Hardware: {', '.join(self.hardware_compatibility)}")
        if self.decoders:
            lines.append(f"  Decoders: {', '.join(self.decoders)}")
        if self.noise_models:
            lines.append(f"  Noise models: {', '.join(self.noise_models)}")
        if self.logical_gates:
            lines.append(f"  Logical gates: {', '.join(self.logical_gates)}")

        lines.append(f"  Fault tolerant: {'Yes' if self.fault_tolerant else 'No'}")
        lines.append(f"  Magic state distillation: {'Yes' if self.magic_state_distillation else 'No'}")
        lines.append(f"{'─' * 60}")
        lines.append(f"  {self.description}")

        if self.key_papers:
            lines.append(f"{'─' * 60}")
            lines.append("  Key Papers:")
            for p in self.key_papers:
                authors = ", ".join(p.authors[:3])
                if len(p.authors) > 3:
                    authors += " et al."
                lines.append(f"    {authors} ({p.year}) — {p.title}")
                lines.append(f"    arxiv: {p.arxiv}")

        lines.append(f"{'=' * 60}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Return raw dictionary representation of this code."""
        return self.model_dump()

    def to_export_config(self) -> dict:
        """Return a dict formatted for downstream Qorex tool consumption."""
        from qlex import __version__

        return {
            "code_id": self.id,
            "code_name": self.name,
            "parameters": self.parameters.model_dump(),
            "supported_noise_models": list(self.noise_models),
            "recommended_decoders": list(self.decoders),
            "threshold_reference": self.threshold.model_dump(),
            "qlex_version": __version__,
        }
