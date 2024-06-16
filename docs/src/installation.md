# Installation

!!! warning
    Please note that `ffmpeg` is not shipped with `pffmpeg`.
    You must install it on your system [:octicons-link-external-24:](https://ffmpeg.org/){ target="_blank" }.

:material-arrow-right-circle: Python ≥ 3.10 is required.

PFFmpeg is available as `pffmpeg` on PyPI:

## Pip from PyPI

You can install `ffmpeg` easily with `pip`:

<!-- termynal -->

```bash
$ pip install pffmpeg
---> 100%
Installed!
```

!!! tip
    The use of a virtual environment is greatly recommended, don’t install in your global python environment.</br>
    You can at least use `--user` to avoid installing system-wide :material-shield-check:.

## Pip from GitHub

If you want to install from source, you can install from the GitHub repo:

<!-- termynal -->

```bash
$ pip install git+https://github.com/CGuichard/ispec.git@main
---> 100%
Installed from source!
```

## Pipx from PyPI

The most elegant way to install `pffmpeg` is to use the tool named Pipx.

Pipx install Python "applications" in isolated environments, and expose things like the CLI to the user environment.
[Learn more :octicons-link-external-24:](https://pipx.pypa.io/){ target="_blank" }.

Install with `pipx`:

<!-- termynal -->

```bash
$ pipx install pffmpeg
---> 100%
Installed in isolated environment!
```
