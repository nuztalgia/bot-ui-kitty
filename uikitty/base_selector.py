from collections.abc import Callable
from typing import Any, Final

from discord import Interaction
from discord.ui import View


class BaseSelector(View):
    """Base class for views that let the user pick from a set of predefined options."""

    def __init__(
        self,
        log: Callable[[str], None] | None,
        options: dict[str, Any],
    ) -> None:
        """Initializes a new `BaseSelector` instance.

        Note:
            In practice, this should only be called via `super()` from subclasses.

        Args:
            log:
                A function that will be called to display information in the console.
                Set to `None` to disable console output for this instance.
            options:
                A dictionary that maps option keys (i.e. names/labels) to option values.
        """
        super().__init__(timeout=None)

        def _log(message: str) -> None:
            if log:
                log(message)

        self.log: Final[Callable[[str], None]] = _log
        self.options: Final[dict[str, Any]] = options
        self.selected_value: Any = None

    async def finish(self, selected_key: str, interaction: Interaction) -> None:
        """Sets this instance's `selected_value` to the value for the `selected_key`.

        Subclasses should rely on this method to call `stop()` and ensure
        that an appropriate value is available for subsequent consumers.

        Args:
            selected_key:
                The `options` dictionary key for the item that was selected by the user.
            interaction:
                The `Interaction` on the UI component that triggered this method call.

        Raises:
            KeyError: If `selected_key` is not in this instance's `options` dictionary.
        """
        await interaction.response.defer()
        self.log(f"└── {interaction.user} selected '{selected_key}'.")
        self.selected_value = self.options[selected_key]
        self.stop()
