"""UI state machine for the QLEX terminal UI."""

from __future__ import annotations

import time
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qlex.models import QECCode


class Screen(Enum):
    """Available screens in the QLEX terminal UI."""

    SPLASH = "SPLASH"
    BROWSE = "BROWSE"
    DETAIL = "DETAIL"
    SEARCH = "SEARCH"
    COMPARE = "COMPARE"
    HELP = "HELP"


class UIState:
    """Manages all application state for the QLEX terminal UI."""

    def __init__(self) -> None:
        self.current_screen: Screen = Screen.SPLASH
        self.selected_index: int = 0
        self.scroll_offset: int = 0
        self.search_query: str = ""
        self.search_mode: bool = False
        self.compare_selection: list[str] = []
        self.active_code: QECCode | None = None
        self.filter_family: str | None = None
        self.message: str = ""
        self.message_time: float = 0.0
        self.should_animate: bool = False

    def transition_to(self, screen: Screen) -> None:
        """Set the current screen and flag for transition animation."""
        self.should_animate = True
        self.current_screen = screen

    def set_message(self, msg: str) -> None:
        """Set a transient status message that clears after 2 seconds."""
        self.message = msg
        self.message_time = time.time()

    def get_message(self) -> str:
        """Return the current message if still within its display window."""
        if self.message and (time.time() - self.message_time) < 2.0:
            return self.message
        self.message = ""
        return ""

    def toggle_compare(self, code_id: str) -> None:
        """Toggle a code ID in/out of the compare selection (max 3)."""
        if code_id in self.compare_selection:
            self.compare_selection.remove(code_id)
            self.set_message(f"Removed {code_id} from compare")
        elif len(self.compare_selection) < 3:
            self.compare_selection.append(code_id)
            self.set_message(f"Staged {code_id} for compare ({len(self.compare_selection)}/3)")
        else:
            self.set_message("Compare is full (max 3)")
