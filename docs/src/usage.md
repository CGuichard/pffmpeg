# Usage

You can use any `ffmpeg` command with `pffmpeg`:

<!-- termynal -->

```bash
$ pffmpeg -h
# Print help

$ pffmpeg -version
# Print version

$ pffmpeg -i input.mp4 output.mp4
# Video processing
```

Most of the commands should be unaffected by the usage of `pffmpeg`, only
processing operations will have a progress bar replacing standard output.

## Comparison with/without

Demo with FFmpeg:

![Demo ffmpeg](./assets/img/demo-ffmpeg.gif){ class="terminal-gif" }

Demo with **P**FFmpeg:

![Demo pffmpeg](./assets/img/demo-pffmpeg.gif){ class="terminal-gif" }

## Limits

Because PFFmpeg uses the output of FFmpeg to work, the flag `-nostats` cannot be used,
and will be ignored by PFFmpeg.
In the same fashion, setting the log level with `-v/-loglevel` below "info" will also be ignored.
