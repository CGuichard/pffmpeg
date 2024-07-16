#!/usr/bin/env python
"""Print release notes for latest version."""

import argparse
import pathlib
import re
import sys

CHANGELOG_PATH = pathlib.Path("CHANGELOG.md")
LATEST_RELEASE_PATTERN = re.compile(
    r"(## \d+\.\d+\.\d+ \(\d{4}-\d{2}-\d{2}\)\n\n.+?)(?=\n\n## |\Z)",
    re.DOTALL,
)
VERSION_HEADER = re.compile(r"## (\d+\.\d+\.\d+) (\(\d{4}-\d{2}-\d{2}\))")
MD_HEADER = re.compile(r"^(#+) (.*)\n\n", re.MULTILINE)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tag-msg",
        action="store_true",
        help="Print release message for git tag.",
    )
    parser.add_argument(
        "-g",
        "--github-release",
        action="store_true",
        help="Print release notes for GitHub.",
    )
    args = parser.parse_args()

    changelog = CHANGELOG_PATH.read_text()

    # Retrieve release notes
    latest_release_match = LATEST_RELEASE_PATTERN.search(changelog)
    if not latest_release_match:
        sys.exit(-1)
    content = latest_release_match.group().strip()

    # Retrieve version
    version_match = VERSION_HEADER.search(content)
    if not version_match:
        sys.exit(-1)
    version = version_match.group(1)

    if args.tag_msg:
        content = content.replace(
            version_match.group(), f"## Version {version}"
        ).lstrip()
        for m in MD_HEADER.finditer(content):
            header_level = len(m.group(1))
            header = m.group(2)
            match header_level:
                case 2:
                    content = content.replace(
                        m.group(), f"{header}\n{'-' * len(header)}\n\n", 1
                    )
                case 3:
                    content = content.replace(m.group(), f"{header}:\n", 1)

    elif args.github_release:
        content = content.replace(version_match.group(), "## Release Notes").lstrip()
        content += (
            "\n\n## Artifacts\n\nThe wheel and sdist of the release "
            "can be found below."
        )

    if content:
        print(content)
    else:
        sys.exit(-1)
