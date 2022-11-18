from importlib.metadata import version
from pathlib import Path
from typing import Any, Final

from botstrap import Botstrap, CliColors, Color, Option
from discord import Bot


class UiKittyBot(Bot):
    def __init__(self, parent_dir: Path, force_sync: bool, **options: Any) -> None:
        super().__init__(**options)
        self._force_sync: Final[bool] = force_sync

        for file_path in parent_dir.glob("*.py"):
            if file_path.stem != "bot":
                print(f"Loading extension '{file_path.stem}'.")
                self.load_extension(file_path.stem)

    async def on_ready(self) -> None:
        if self._force_sync:
            print("Force-syncing commands. Be mindful of the rate limit.")
            await self.sync_commands(force=True)

        print("UI Kitty is online and ready!")


def main() -> int:
    parent_dir = Path(__file__).parent

    botstrap = Botstrap(
        name := "bot-ui-kitty",
        version=version(name),
        colors=CliColors(primary=Color.pink),
    ).register_token("main", storage_directory=parent_dir)

    args = botstrap.parse_args(
        force_sync=Option(flag=True, help="Force-sync application commands."),
    )
    botstrap.run_bot(
        bot_class=UiKittyBot,
        parent_dir=parent_dir,
        force_sync=args.force_sync,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
