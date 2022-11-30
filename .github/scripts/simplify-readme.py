"""This script simplifies the project README to avoid confusing PyPI with formatting."""

import re
from pathlib import Path


def get_github_link(header: str) -> str:
    return (
        f"https://github.com/nuztalgia/bot-ui-kitty#{header.lower().replace(' ', '-')}"
    )


def main() -> int:
    readme_file = (Path(__file__) / "../../../README.md").resolve()
    readme_text = readme_file.read_text()

    # Currently, "Available Views" is the only section that needs to be simplified.
    available_views_match = re.search(
        r"## Available Views\n\n(.+)\n## [A-Z]", readme_text, flags=re.DOTALL
    )

    if not available_views_match:
        print("Could not find 'Available Views' section in 'README.md'.")
        return 1

    original_text = (txt := available_views_match.group(1))[: txt.rindex("\n ")].strip()

    # The header for each view type will link to the corresponding header on GitHub.
    partially_simplified_text = re.sub(
        r"^### ([a-zA-Z ]+)$",
        lambda match: f"### [{match.group(1)}]({get_github_link(match.group(1))})",
        original_text,
        flags=re.MULTILINE,
    )

    # Each "Example" bullet point will only contain a single image and a code snippet.
    fully_simplified_text = re.sub(
        r"(- \*+Example.+?)\n.+?(https://user-images.+?\.png).+?```",
        lambda match: f"{match.group(1)}\n\n  ![image]({match.group(2)})\n\n  ```",
        partially_simplified_text,
        flags=re.DOTALL,
    )

    readme_file.write_text(readme_text.replace(original_text, fully_simplified_text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
