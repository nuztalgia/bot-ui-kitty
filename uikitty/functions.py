"""Top-level functions that provide UI views and abstract away the underlying machinery.

This module is star-imported into `__init__.py` (i.e. `from uikitty.functions import *`)
and therefore effectively serves as the public API surface for this package.

All functions in this module must be thoroughly documented and (relatively) easy to use,
and should (if feasible/applicable) provide reasonable options for user customization.
"""

from collections.abc import Callable
from typing import Any

from discord import ApplicationContext, ButtonStyle, Embed

from uikitty.dynamic_selector import DynamicSelector


async def dynamic_select(
    ctx: ApplicationContext,
    *args: str,
    content: str | None = None,
    embed: Embed | None = None,
    button_style: ButtonStyle = ButtonStyle.secondary,
    select_placeholder: str | None = None,
    log: Callable[[str], None] | None = print,
    **kwargs: Any,
) -> Any:
    """Displays a collection of options and returns the one selected by the user.

    Note:
        The appearance/behavior of the view rendered by this function (if any)
        is determined by the number of options that are provided:

        - If there are **no** options, this function will simply return `None`.

        - If there is **exactly 1** option, this function will return that option (if
          specified via `*args`) or the option's value (if specified via `**kwargs`).

        - If there are **between 2 and 5** options (inclusive), they will be displayed
          as a single row of `Button` components (one button per option). This function
          will return the selected option (or its value) once the user clicks a button.

        - If there are **between 6 and 25** options (inclusive), they will be displayed
          in a single `Select` component. This function will return the selected option
          (or its value) once the user clicks an item in the dropdown menu.

        - If there are **26 or more** options, they will be evenly divided into pages
          and displayed in a composite `Paginator` view. This function will return the
          selected option (or its value) once the user selects it (using the `Select`
          component) and confirms their choice (using the central `Button` component).

    Args:
        ctx:
            The context for the application command that prompted this selection.
        *args:
            An ordered collection of option strings.
            Cannot be used alongside `**kwargs`.
        content:
            The text content to display in the message with the selector view.
            Optional. May be used alongside `embed`.
        embed:
            An embed to display in the message with the selector view.
            Optional. May be used alongside `content`.
        button_style:
            The `ButtonStyle` to use for the option `Button` components.
            Only applicable if there are between 2 and 5 options (inclusive).
        select_placeholder:
            The placeholder text to display in the `Select` (dropdown) component.
            Only applicable if there are between 6 and 25 options (inclusive).
        log:
            A function that will be called to display debug information in the console.
            Set to `None` to disable console output for this function call.
        **kwargs:
            An ordered mapping of option labels to option values.
            Cannot be used alongside `*args`.

    Returns:
        The user's selected option string (if `*args`) or option value (if `**kwargs`).
    """
    if args and kwargs:
        raise ValueError(
            "Either '*args' or '**kwargs' (not both!) "
            "must be provided to define the available options."
        )

    options = kwargs if kwargs else {arg: arg for arg in args}

    if len(options) < DynamicSelector.MIN_OPTIONS:
        return next(iter(options.values())) if options else None

    view = DynamicSelector(ctx, button_style, select_placeholder, log, options)
    respond = ctx.edit if ctx.response.is_done() else ctx.respond

    await respond(content=content, embed=embed, view=view)
    await view.wait()

    return view.selected_value
