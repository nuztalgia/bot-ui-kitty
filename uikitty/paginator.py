import functools
from collections.abc import Callable, Coroutine
from typing import Any, Final, NamedTuple

from discord import ApplicationContext, ButtonStyle, Interaction, SelectOption
from discord.ui import Button, Select

from uikitty.base_selector import BaseSelector


class Paginator:
    """A helper class that displays and manages paginated options for a `BaseSelector`.

    This class must be initialized with an `int` signaling how many pages to display, as
    well as a corresponding number of lists of `SelectOption` items (where each `list`
    represents the options that should be rendered on its page).

    After an instance of this class is created, its `attach()` method must be called in
    order to make it functional. The provided `BaseSelector`'s `finish()` method will be
    called asynchronously once the user selects an option and confirms their choice.
    """

    class UI(NamedTuple):
        """A `NamedTuple` containing the individual UI components in a `Paginator`."""

        select: Select = Select()
        """A dropdown menu containing all the available options on the current page."""

        prev_button: Button = Button(style=ButtonStyle.primary, label="<<")
        """Navigates to the previous page when clicked. Disabled when on first page."""

        center_button: Button = Button()
        """Confirms the selected option when clicked. Disabled if no option is selected.
           While disabled, will show information about the current pagination state."""

        next_button: Button = Button(style=ButtonStyle.primary, label=">>")
        """Navigates to the next page when clicked. Disabled when on last page."""

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
