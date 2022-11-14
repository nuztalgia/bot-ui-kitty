from collections.abc import Callable
from typing import Any

from discord import ApplicationContext, ButtonStyle, Embed

from uikitty.dynamic_selector import MIN_OPTIONS_FOR_UI, DynamicSelector


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
    if args and kwargs:
        raise ValueError(
            "Either '*args' or '**kwargs' (not both!) "
            "must be provided to define the available options."
        )

    options = kwargs if kwargs else {arg: arg for arg in args}

    if len(options) < MIN_OPTIONS_FOR_UI:
        return next(iter(options.values())) if options else None

    view = DynamicSelector(ctx, button_style, select_placeholder, log, options)
    respond = ctx.edit if ctx.response.is_done() else ctx.respond

    await respond(content=content, embed=embed, view=view)
    await view.wait()

    return view.selected_value
