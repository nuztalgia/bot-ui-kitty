import functools
from collections.abc import Callable, Coroutine
from typing import Any, Final, NamedTuple

from discord import ApplicationContext, ButtonStyle, Interaction, SelectOption
from discord.ui import Button, Select

from uikitty.base_selector import BaseSelector


class Paginator:
    class UI(NamedTuple):
        select: Select = Select()
        prev_button: Button = Button(style=ButtonStyle.primary, label="<<")
        center_button: Button = Button()
        next_button: Button = Button(style=ButtonStyle.primary, label=">>")

    def __init__(
        self,
        page_count: int,
        *options_by_page: list[SelectOption],
        placeholder: str = "Make a selection, or use the arrows for more options",
    ) -> None:
        if page_count != len(options_by_page):
            raise ValueError("Length of 'options_by_page' does not match 'page_count'.")

        self.page_count: Final[int] = page_count
        self.options_by_page: Final[tuple[list[SelectOption], ...]] = options_by_page
        self.default_placeholder: Final[str] = placeholder
        self.ui: Final[Paginator.UI] = type(self).UI()

        self.ui.select.callback = self.on_select
        self.ui.prev_button.callback = self.on_prev_click
        self.ui.next_button.callback = self.on_next_click

        async def uninitialized() -> None:
            raise RuntimeError("'self.refresh_view' was never properly initialized.")

        self.refresh_view: Callable[[], Coroutine[Any, Any, None]] = uninitialized
        self.current_page: int = 0
        self.current_selection: str | None = None

    def attach(self, parent_view: BaseSelector, ctx: ApplicationContext) -> None:
        async def on_confirm(interaction: Interaction) -> None:
            if isinstance(self.current_selection, str):
                await parent_view.finish(self.current_selection, interaction)
            else:
                raise TypeError("Cannot confirm a nonexistent selection.")

        self.refresh_view = functools.partial(ctx.edit, view=parent_view)
        self.ui.center_button.callback = on_confirm
        self.update_ui()

        for component in self.ui:
            parent_view.add_item(component)

    @property
    def has_selection(self) -> bool:
        return self.current_selection is not None

    async def on_select(self, interaction: Interaction) -> None:
        self.current_selection = self.ui.select.values[0]
        await self.on_interaction(interaction)

    async def on_prev_click(self, interaction: Interaction) -> None:
        self.current_page -= 1
        self.current_selection = None
        await self.on_interaction(interaction)

    async def on_next_click(self, interaction: Interaction) -> None:
        self.current_page += 1
        self.current_selection = None
        await self.on_interaction(interaction)

    async def on_interaction(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        self.update_ui()
        await self.refresh_view()

    def update_ui(self) -> None:
        options = self.options_by_page[self.current_page]
        center_button_label = f"Page {self.current_page + 1} of {self.page_count}"

        if self.has_selection:
            self.ui.select.placeholder = self.current_selection
            self.ui.select.options = [
                option for option in options if (option.label != self.current_selection)
            ]
            self.ui.center_button.style = ButtonStyle.success
            self.ui.center_button.label = "Confirm Selection"
            self.ui.center_button.disabled = False
        else:
            self.ui.select.placeholder = self.default_placeholder
            self.ui.select.options = options
            self.ui.center_button.style = ButtonStyle.secondary
            self.ui.center_button.label = center_button_label
            self.ui.center_button.disabled = True

        self.ui.prev_button.disabled = self.current_page == 0
        self.ui.next_button.disabled = self.current_page == (self.page_count - 1)
