# PFFmpeg

<div align="center" style="margin:40px;">

<img src="https://raw.githubusercontent.com/CGuichard/pffmpeg/main/docs/src/assets/img/logo.png" alt="PFFmpeg logo" style="margin-bottom: 20px" width="300"/>

_Progress bar for FFmpeg_

<!-- --8<-- [start:badges] -->
[![Language](https://img.shields.io/badge/language-python≥3.10-3776ab?style=flat-square)](https://www.python.org/)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)
[![Documentation](https://img.shields.io/badge/documentation-Material%20for%20MkDdocs-0a507a?style=flat-square)](https://CGuichard.github.io/pffmpeg/)
![Style](https://img.shields.io/badge/style-ruff-9a9a9a?style=flat-square)
![Lint](https://img.shields.io/badge/lint-ruff,%20mypy-brightgreen?style=flat-square)
![Security](https://img.shields.io/badge/security-bandit,%20pip--audit-purple?style=flat-square)
[![PyPI - Version](https://img.shields.io/pypi/v/pffmpeg?style=flat-square)](https://pypi.org/project/pffmpeg/)
[![Tests](https://img.shields.io/github/actions/workflow/status/CGuichard/pffmpeg/check.yml?branch=main&label=Test)](https://github.com/CGuichard/pffmpeg/actions/workflows/check.yml)
[![Coverage](https://raw.githubusercontent.com/CGuichard/pffmpeg/refs/heads/gh-tests-coverages/data/main/badge.svg)](https://github.com/CGuichard/pffmpeg/actions/workflows/check.yml)

[Pull Request](https://github.com/CGuichard/pffmpeg/pulls) **·**
[Bug Report](https://github.com/CGuichard/pffmpeg/issues/new?template=bug_report.md) **·**
[Feature Request](https://github.com/CGuichard/pffmpeg/issues/new?template=feature_request.md)
<!-- --8<-- [end:badges] -->

</div>

---

**Documentation**: <a href="https://cguichard.github.io/pffmpeg" target="_blank">https://cguichard.github.io/pffmpeg</a>

**Source Code**: <a href="https://github.com/CGuichard/pffmpeg" target="_blank">https://github.com/CGuichard/pffmpeg</a>

---

<!-- --8<-- [start:introduction] -->

The FFmpeg command line tool is a universal media converter. It can read a wide variety of inputs,
filter and transcode them into a plethora of output formats. For new user it can be extremely
convoluted to use, and read the output. When converting a video file for the first time,
understanding the progress of the current task from the output is quite the confusing task.

This is where PFFmpeg comes in. It's CLI is just on top of FFmpeg's, and delegates everything to it.
The output of the FFmpeg is parsed and "patched" to display a progress bar while running an action
such as a video compression. PFFmpeg philosophy is to alter as little as possible the FFmpeg experience,
and simply add the progress bar when needed, unlike other project who just wrap and hide all of the
output behind a progress bar. In terms of style, the
[`rich`](https://rich.readthedocs.io/en/latest/progress.html) progress bar was chosen.

<!-- --8<-- [end:introduction] -->

## Table of Contents

- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Getting started

### Installation

Install `pffmpeg` with pip:

```bash
pip install pffmpeg
```

Install `pffmpeg` with pip from source:

```bash
pip install git+https://github.com/CGuichard/pffmpeg.git
# pip install git+https://github.com/CGuichard/pffmpeg.git@<tag>
```

### Usage

You can use any `ffmpeg` command with `pffmpeg`:

```bash
# Print help
pffmpeg -h

# Print version
pffmpeg -version

# Video processing
pffmpeg -i input.mp4 output.mp4
```

Demo:

![Demo pffmpeg](./docs/src/assets/img/demo-pffmpeg.gif)

## Contributing

If you want to contribute to this project please check [CONTRIBUTING.md](CONTRIBUTING.md).

Everyone contributing to this project is expected to treat other people with respect,
and more generally to follow the guidelines articulated by our [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

Copyright &copy; 2026, Clément GUICHARD

PFFmpeg is licensed under the MIT license. A copy of this license is provided in the [LICENSE](./LICENSE) file.

## Acknowledgements

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
from the project template [CGuichard/cookiecutter-pypackage](https://github.com/CGuichard/cookiecutter-pypackage).
