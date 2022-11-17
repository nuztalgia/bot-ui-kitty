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

## Components

- [Dynamic Selector](https://github.com/nuztalgia/bot-ui-kitty/blob/aa9d33d7dc2e6658a93c45a8a48a85aaf74d5b96/uikitty/functions.py#L9-L36)

_Screenshots and usage info coming soon!_

## License

Copyright © 2022 [Nuztalgia](https://github.com/nuztalgia). Released under the
[Apache License, Version 2.0][license].

[license]: https://github.com/nuztalgia/bot-ui-kitty/blob/main/LICENSE
