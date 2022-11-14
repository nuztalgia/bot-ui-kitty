from collections.abc import Callable
from typing import Any, Final

from discord import Interaction
from discord.ui import View


class BaseSelector(View):
    def __init__(
        self,
        log: Callable[[str], None] | None,
        options: dict[str, Any],
    ) -> None:
        super().__init__(timeout=None)

        def _log(message: str) -> None:
            if log:
                log(message)

        self.log: Final[Callable[[str], None]] = _log
        self.options: Final[dict[str, Any]] = options
        self.selected_value: Any = None

    async def finish(self, selected_key: str, interaction: Interaction) -> None:
        await interaction.response.defer()
        self.log(f"└── {interaction.user} selected '{selected_key}'.")
        self.selected_value = self.options[selected_key]
        self.stop()
