# 😻 Bot UI Kitty

[![Development Status](https://img.shields.io/pypi/status/bot-ui-kitty)](https://pypi.org/project/bot-ui-kitty/)
[![Latest Version on PyPI](https://img.shields.io/pypi/v/bot-ui-kitty)](https://pypi.org/project/bot-ui-kitty/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/bot-ui-kitty)](https://pypi.org/project/bot-ui-kitty/)
[![Build Status](https://img.shields.io/github/workflow/status/nuztalgia/bot-ui-kitty/Build)](https://github.com/nuztalgia/bot-ui-kitty/actions/workflows/build.yml)
[![CodeQL Status](https://img.shields.io/github/workflow/status/nuztalgia/bot-ui-kitty/CodeQL?label=codeQL)](https://github.com/nuztalgia/bot-ui-kitty/actions/workflows/codeql.yml)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/nuztalgia/bot-ui-kitty/main?label=codefactor)](https://www.codefactor.io/repository/github/nuztalgia/bot-ui-kitty)

A collection of reusable, dynamic, and intuitive Discord UI views, built on top
of Pycord's [**Bot UI Kit**](https://docs.pycord.dev/en/master/api/ui_kit.html).

This project was originally created for personal use in my (way too many)
Discord bots, but I decided to make it more easily accessible just in case other
bot developers find it helpful. 💜

Currently, the only supported Discord library is **[Pycord]**, because that's
the one that most of my bots happen to use. I'm planning to extend support to
other libraries too, but I'm not sure when I'll be able to make the time to do
so. 📚 In the meantime, if you're using a different library, check out my other
utility kit for Discord bots – **[Botstrap]**!

[pycord]: https://github.com/Pycord-Development/pycord
[botstrap]: https://github.com/nuztalgia/botstrap

[**Contributions**][1] to this project are very welcome, as long as they
[pass](https://results.pre-commit.ci/latest/github/nuztalgia/bot-ui-kitty/main)
[all](https://github.com/nuztalgia/bot-ui-kitty/actions/workflows/build.yml)
[the](https://github.com/nuztalgia/bot-ui-kitty/actions/workflows/codeql.yml)
[checks](https://www.codefactor.io/repository/github/nuztalgia/bot-ui-kitty) to
keep it green and healthy. ✅

[1]: https://github.com/nuztalgia/bot-ui-kitty/blob/main/.github/contributing.md

## Installation

```
pip install -U bot-ui-kitty
```

**Note:** Python **3.10** is required (because Pycord doesn't officially support
Python 3.11... [yet]!)

[yet]: https://github.com/Pycord-Development/pycord/blob/master/CHANGELOG.md

### For Development

```
git clone https://github.com/nuztalgia/bot-ui-kitty.git
cd bot-ui-kitty
pip install -e .
```

This will create an [editable installation] of `bot-ui-kitty` in your current
environment. Any changes you make to the code will immediately take effect, so
using a [virtual env] is highly recommended.

[editable installation]:
  https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[virtual env]: https://docs.python.org/3/tutorial/venv.html

## Available Views

### Dynamic Select

This view is designed to handle any use case that calls for selecting a single
item from a sequence of possible options. It'll automatically choose to display
either a row of buttons, a dropdown menu, or a combination of both (to emulate
pagination) depending on the **number of options** you throw at it! 🤹

- **Example 1:** Choose your starter Pokemon! (**3** options)

  <img align="left" src="https://user-images.githubusercontent.com/95021853/202794482-60a5ca50-7593-4f66-a160-3ba1509d4d84.png">

  And after clicking the <kbd>💧 Squirtle</kbd> button...

  ![image](https://user-images.githubusercontent.com/95021853/202794731-4586fcfd-e59d-42d2-b3d4-8bb410b8def7.png)

  ```py
  number = await uikitty.dynamic_select(
      ctx,
      content="Choose your starter Pokemon!",
      **{"🌱 Bulbasaur": 1, "🔥 Charmander": 4, "💧 Squirtle": 7},
  )
  await ctx.edit(content=f"Your Pokemon's number is **#00{number}**!", view=None)
  ```

  ***

- **Example 2:** What time is it, Mr. Wolf? (**24** options)

  <img align="right" src="https://user-images.githubusercontent.com/95021853/202796751-5f541611-4806-4918-ad34-aa347f92b807.png" width=300>

  ![image](https://user-images.githubusercontent.com/95021853/202798098-196a1976-c326-4096-870a-89593f613fa1.png)

  <details>
  <summary>
  This selection appears as a dropdown menu... but no matter what time it is,
  this particular wolf is always hungry! <i>(Click to see spoilers.)</i><p></p>
  </summary>
  <img src="https://user-images.githubusercontent.com/95021853/202798702-cb7d88e1-4c6e-488e-aa0a-5a93e969a2a3.png">
  </details>

  ```py
  time = await uikitty.dynamic_select(
      ctx,
      *[f"{str(i).zfill(2)}:00" for i in range(24)],
      select_placeholder="What time is it, Mr. Wolf?",
  )
  await ctx.edit(content=f"It's ~~{time}~~ **DINNER TIME!!!**", view=None)
  ```

  ***

- **Example 3:** I heard you like chemistry... (**119** options)

  <img align="right" src="https://user-images.githubusercontent.com/95021853/202812334-ac9ee8a9-3083-4276-b0b2-edbcf8cef30e.png">

  This is where things get interesting! ✨

  - When you pass more than 25 options into a **Dynamic Select** view, they'll
    be evenly divided into "pages".
  - The options for the current page are displayed in the dropdown menu.
  - You can change the current page by clicking the <kbd><<</kbd> and
    <kbd>>></kbd> buttons.

  Here's what this example looks like on the first page, middle page, and last
  page. Notice that the <kbd><<</kbd> button is disabled on the first page, the
  <kbd>>></kbd> button is disabled on the last page, and the center button is
  always disabled.

  <img align="left" src="https://user-images.githubusercontent.com/95021853/202810734-38a2bbaa-dc09-49d5-985b-2e79083c8ecc.png" width=250>
  <img align="right" src="https://user-images.githubusercontent.com/95021853/202811225-7e02d68e-1865-4bff-9d0e-dd43f1bcbfe8.png" width=250>
  <p align="center"><img src="https://user-images.githubusercontent.com/95021853/202811048-1804731c-4f9d-455c-9137-ce4a02850b01.png" width=250></p>

  When you select an option in the dropdown, the center button will light up,
  allowing you to confirm your choice.

  <img align="right" src="https://user-images.githubusercontent.com/95021853/202820828-89776e90-fc09-45d3-a95f-3dbdb06cedbc.png" height=212>

  ![image](https://user-images.githubusercontent.com/95021853/202818792-4554f2a7-ec01-4057-9537-2c398a020ebf.png)

  ```py
  element = await uikitty.dynamic_select(
      ctx,
      embed=Embed(title="Select an element to learn more about it!", color=color),
      **elements_data,
  )
  embed = Embed(
      title=element["name"], description=element["summary"], url=element["source"],
  )
  await ctx.edit(embed=embed, view=None)
  ```

  **Note:** `elements_data` in the above snippet is sourced from
  [Bowserinator/Periodic-Table-JSON][periodic-table-json].

[periodic-table-json]: https://github.com/Bowserinator/Periodic-Table-JSON

## License

Copyright © 2022 [Nuztalgia](https://github.com/nuztalgia). Released under the
[Apache License, Version 2.0][license].

[license]: https://github.com/nuztalgia/bot-ui-kitty/blob/main/LICENSE
