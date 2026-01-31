# Installation

!!! warning
    Please note that `ffmpeg` is not shipped with `pffmpeg`.
    You must install it on your system [:octicons-link-external-24:](https://ffmpeg.org/){ target="_blank" }.

:material-arrow-right-circle: Python ≥ 3.10 is required.

PFFmpeg is available as `pffmpeg` on PyPI.

## Pip

You can install `pffmpeg` easily with `pip`:

<!-- termynal -->

```bash
$ pip install pffmpeg
---> 100%
Installed!
```

!!! tip
    The use of a virtual environment is greatly recommended :material-shield-check:.

You can install from the repository:

<!-- termynal -->

```bash
$ pip install git+https://github.com/CGuichard/pffmpeg.git@main
---> 100%
Installed from source!
```

## Pipx

Pipx is a tool that let you install and run Python "applications" in isolated
environments, and exposes the commands in your user environment.

You can install `pffmpeg` with `pipx`:

<!-- termynal -->

```bash
$ pipx install pffmpeg
---> 100%
Installed in isolated environment!
```

!!! info
    Learn more about [Pipx :octicons-link-external-24:](https://pipx.pypa.io/){ target="_blank" }.

## UV

UV is an extremely fast Python package and project manager. One of its features is "Tools",
that exposes commands from Python packages just like Pipx.

You can install `pffmpeg` with `uv tool`:

<!-- termynal -->

```bash
$ uv tool install pffmpeg
---> 100%
Installed!
```

!!! info
    Learn more about [uv :octicons-link-external-24:](https://docs.astral.sh/uv/){ target="_blank" }
    and [uv tool :octicons-link-external-24:](https://docs.astral.sh/uv/concepts/tools/){ target="_blank" }.
