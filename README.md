# PFFmpeg

<div align="center" style="margin:40px;">
  <img src="https://raw.githubusercontent.com/CGuichard/pffmpeg/main/docs/src/assets/img/logo.png" alt="PFFmpeg logo" style="margin-bottom: 20px" width="300"/>

  _Progress bar for FFmpeg_

  <!-- --8<-- [start:overview-header] -->
  [![Language](https://img.shields.io/badge/Language-python≥3.10-3776ab?style=flat-square&logo=Python)](https://www.python.org/)
  ![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
  [![Documentation](https://img.shields.io/badge/Documentation-mkdocs-0a507a?style=flat-square)](https://cguichard.github.io/pffmpeg/)
  ![Style](https://img.shields.io/badge/Style-ruff-9a9a9a?style=flat-square)
  ![Lint](https://img.shields.io/badge/Lint-ruff,%20mypy-brightgreen?style=flat-square)
  ![Security](https://img.shields.io/badge/Security-bandit,%20pip%20audit-purple?style=flat-square)
  [![Tests](https://github.com/CGuichard/pffmpeg/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/CGuichard/pffmpeg/actions/workflows/tests.yml)

  [Pull Request](https://github.com/CGuichard/pffmpeg/pulls) **·**
  [Bug Report](https://github.com/CGuichard/pffmpeg/issues/new?template=bug_report.md) **·**
  [Feature Request](https://github.com/CGuichard/pffmpeg/issues/new?template=feature_request.md)
  <!-- --8<-- [end:overview-header] -->

</div>

<!-- --8<-- [start:overview-body] -->
---

**Documentation**: <a href="https://cguichard.github.io/pffmpeg" target="_blank">https://cguichard.github.io/pffmpeg</a>

**Source Code**: <a href="https://github.com/CGuichard/pffmpeg" target="_blank">https://github.com/CGuichard/pffmpeg</a>

---

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

<!-- --8<-- [end:overview-body] -->
## Table of Contents

- [Quick start](#quick-start)
- [Contributing](#contributing)
- [License](#license)

## Quick start

Install PFFmpeg with pip (from PyPI):

```bash
pip install pffmpeg
```

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

If you want to contribute to this project or understand how it works,
please check [CONTRIBUTING.md](CONTRIBUTING.md).

Any contribution is greatly appreciated.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more
information.
