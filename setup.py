from setuptools import setup

setup(
    url="https://github.com/nuztalgia/bot-ui-kitty",
    project_urls={
        "Issue Tracker": "https://github.com/nuztalgia/bot-ui-kitty/issues",
        "Source Code": "https://github.com/nuztalgia/bot-ui-kitty/tree/main/uikitty",
    },
    install_requires=[
        "py-cord ==2.3.1",
    ],
    use_scm_version={
        "local_scheme": lambda version: str(version.tag),
        "version_scheme": lambda _: "",
    },
)
