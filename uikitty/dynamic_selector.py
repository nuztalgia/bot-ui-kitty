import functools
import math
from collections.abc import Callable
from typing import Any, Final

from discord import ApplicationContext, ButtonStyle, Interaction, SelectOption
from discord.ui import Button, Select

from uikitty.base_selector import BaseSelector
from uikitty.paginator import Paginator

MAX_ENTRIES_PER_SELECT: Final[int] = 25
MAX_BUTTONS_PER_ROW: Final[int] = 5
MIN_OPTIONS_FOR_UI: Final[int] = 2


class DynamicSelector(BaseSelector):
    def __init__(
        self,
        ctx: ApplicationContext,
        button_style: ButtonStyle,
        select_placeholder: str | None,
        log: Callable[[str], None] | None,
        options: dict[str, Any],
    ) -> None:
        super().__init__(log=log, options=options)

        match len(self.options):
            case n if n > MAX_ENTRIES_PER_SELECT:
                page_count = math.ceil(n / MAX_ENTRIES_PER_SELECT)
                self.log(
                    f"Setting up a paginated selector with {n} "
                    f"options spread across {page_count} pages."
                )
                self.setup_paginator(ctx, page_count)
            case n if n > MAX_BUTTONS_PER_ROW:
                self.log(f"Setting up a simple dropdown menu with {n} options.")
                self.setup_simple_select(select_placeholder)
            case n if n >= MIN_OPTIONS_FOR_UI:
                self.log(f"Setting up an action row of {n} buttons.")
                self.setup_simple_buttons(button_style)
            case _:
                raise ValueError(f"At least {MIN_OPTIONS_FOR_UI} options are required.")

    def setup_simple_buttons(self, style: ButtonStyle) -> None:
        for key in self.options:
            button = Button(style=style, label=key)
            button.callback = functools.partial(self.finish, button.label)
            self.add_item(button)

    def setup_simple_select(self, placeholder: str | None) -> None:
        select = Select(
            placeholder=placeholder,
            options=[SelectOption(label=key) for key in self.options],
        )

        async def callback(interaction: Interaction) -> None:
            await self.finish(select.values[0], interaction)

        select.callback = callback
        self.add_item(select)

    def setup_paginator(self, ctx: ApplicationContext, page_count: int) -> None:
        option_keys = list(self.options)
        quot, rmdr = divmod(len(self.options), page_count)

        def get_options(start: int, end: int) -> list[SelectOption]:
            return [SelectOption(label=key) for key in option_keys[start:end]]

        options_by_page = [
            get_options((i * quot) + min(i, rmdr), ((i + 1) * quot) + min(i + 1, rmdr))
            for i in range(page_count)
        ]
        Paginator(page_count, *options_by_page).attach(self, ctx)
