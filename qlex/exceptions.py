"""Custom exceptions for the QLEX library."""


class RegistryError(Exception):
    """Raised when the code registry fails to load or is corrupted."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Registry error: {message}")


class CodeNotFoundError(Exception):
    """Raised when a requested QEC code ID does not exist in the registry."""

    def __init__(self, code_id: str, available_ids: list[str]) -> None:
        ids_str = ", ".join(sorted(available_ids))
        super().__init__(
            f"Code '{code_id}' not found. Available IDs: {ids_str}"
        )
        self.code_id = code_id
        self.available_ids = available_ids


class ComparisonError(Exception):
    """Raised when a comparison operation cannot be performed."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Comparison error: {message}")


class FilterError(Exception):
    """Raised when an invalid filter parameter is provided."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Filter error: {message}")
