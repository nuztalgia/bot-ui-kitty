import json
from typing import Any, Final

from discord import ApplicationContext, Bot, Cog, Embed, SlashCommandGroup

import uikitty


class DynamicSelectCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Final[Bot] = bot
        self.elements_data: Final[dict[str, Any]] = {}

    select = SlashCommandGroup("select", "Examples for the Dynamic Select view.")

    @select.command(
        description="An example of a Dynamic Select view with 3 options.",
    )
    async def pokemon(self, ctx: ApplicationContext) -> None:
        number = await uikitty.dynamic_select(
            ctx,
            content="Choose your starter Pokemon!",
            **{  # type: ignore[arg-type]
                "🌱 Bulbasaur": 1,
                "🔥 Charmander": 4,
                "💧 Squirtle": 7,
            },
        )
        await ctx.edit(content=f"Your Pokemon's number is **#00{number}**!", view=None)

    @select.command(
        description="An example of a Dynamic Select view with 24 options.",
    )
    async def time(self, ctx: ApplicationContext) -> None:
        time = await uikitty.dynamic_select(
            ctx,
            *[f"{str(i).zfill(2)}:00" for i in range(24)],
            select_placeholder="What time is it, Mr. Wolf?",
        )
        await ctx.edit(content=f"It's ~~{time}~~ **DINNER TIME!!!**", view=None)

    @select.command(description="An example of a Dynamic Select view with 119 options.")
    async def element(self, ctx: ApplicationContext) -> None:
        if not self.elements_data:
            await ctx.response.defer()
            await self._fetch_elements()

        color = ctx.guild.me.color
        element = await uikitty.dynamic_select(
            ctx,
            embed=Embed(title="Select an element to learn more about it!", color=color),
            **self.elements_data,
        )
        embed = Embed(
            title=element["name"],
            description=element["summary"],
            url=element["source"],
            color=color,
        )
        await ctx.edit(embed=embed, view=None)

    async def _fetch_elements(self) -> None:
        data_url = (
            "https://raw.githubusercontent.com/Bowserinator/"
            "Periodic-Table-JSON/master/PeriodicTableJSON.json"
        )
        # noinspection PyUnresolvedReferences, PyProtectedMember
        async with self.bot.http._HTTPClient__session.get(data_url) as response:
            elements = json.loads(await response.text())["elements"]

        for element in elements:
            label = f"{element['number']}. {element['name']} ({element['symbol']})"
            self.elements_data[label] = {
                k: v for k, v in element.items() if k in {"name", "source", "summary"}
            }


def setup(bot: Bot) -> None:
    bot.add_cog(DynamicSelectCog(bot))
