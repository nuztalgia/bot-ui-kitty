import functools
from collections.abc import Callable, Coroutine
from typing import Any, Final, NamedTuple

from discord import ApplicationContext, ButtonStyle, Interaction, SelectOption
from discord.ui import Button, Select

from uikitty.base_selector import BaseSelector


class Paginator:
    """A helper class that displays and manages paginated options for a `BaseSelector`.

    This class must be initialized with multiple lists of `SelectOption` items, in which
    each `list` represents the options that should be rendered on an individual page.

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
        *options_by_page: list[SelectOption],
        placeholder: str = "Make a selection, or use the arrows for more options",
    ) -> None:
        """Initializes a new `Paginator` instance.

        Args:
            *options_by_page:
                Lists of `SelectOption` items, in which each `list` represents
                the options that should be rendered on an individual page.
            placeholder:
                The placeholder text to display in the `Select` (dropdown) menu.

        Raises:
            ValueError: If fewer than `2` lists (i.e. pages) of options are provided.
        """
        if len(options_by_page) < 2:
            raise ValueError("At least two lists (i.e. pages) of options are required.")

        self.options_by_page: Final[tuple[list[SelectOption], ...]] = options_by_page
        self.default_placeholder: Final[str] = placeholder
        self.ui: Final[Paginator.UI] = type(self).UI()

        self.ui.select.callback = self._on_select
        self.ui.prev_button.callback = self._on_prev_click
        self.ui.next_button.callback = self._on_next_click

        async def uninitialized() -> None:
            raise RuntimeError("'self.refresh_view' was never properly initialized.")

        self.refresh_view: Callable[[], Coroutine[Any, Any, None]] = uninitialized
        self.current_page: int = 0
        self.current_selection: str | None = None

    def attach(self, parent_view: BaseSelector, ctx: ApplicationContext) -> None:
        """Adds pagination UI components to the view and sets up the required callbacks.

        Args:
            parent_view:
                The `BaseSelector` view to which these UI components will be added.
                Once a selection is made, this view's `finish()` method will be called.
            ctx:
                The context for the application command that prompted this selection.
        """

        async def on_confirm(interaction: Interaction) -> None:
            if isinstance(self.current_selection, str):
                await parent_view.finish(self.current_selection, interaction)
            else:
                raise TypeError("Cannot confirm a nonexistent selection.")

        self.refresh_view = functools.partial(ctx.edit, view=parent_view)
        self.ui.center_button.callback = on_confirm
        self._update_ui()

        for component in self.ui:
            parent_view.add_item(component)

    @property
    def _has_selection(self) -> bool:
        return self.current_selection is not None

    async def _on_select(self, interaction: Interaction) -> None:
        self.current_selection = self.ui.select.values[0]
        await self._on_interaction(interaction)

    async def _on_prev_click(self, interaction: Interaction) -> None:
        self.current_page -= 1
        self.current_selection = None
        await self._on_interaction(interaction)

    async def _on_next_click(self, interaction: Interaction) -> None:
        self.current_page += 1
        self.current_selection = None
        await self._on_interaction(interaction)

    async def _on_interaction(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        self._update_ui()
        await self.refresh_view()

    def _update_ui(self) -> None:
        page_count = len(self.options_by_page)
        options = self.options_by_page[self.current_page]
        center_button_label = f"Page {self.current_page + 1} of {page_count}"

        if self._has_selection:
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
        self.ui.next_button.disabled = self.current_page == (page_count - 1)
