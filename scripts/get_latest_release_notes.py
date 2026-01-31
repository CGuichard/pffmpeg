#!/usr/bin/env python3
"""Print release notes for latest version."""

import argparse
import pathlib
import re
import sys

CHANGELOG_PATH = pathlib.Path("CHANGELOG.md")
RELEASE_PATTERN = re.compile(
    r"(## \d+\.\d+\.\d+ \(\d{4}-\d{2}-\d{2}\)\n\n.+?)(?=\n\n## |\Z)",
    re.DOTALL,
)
VERSION_HEADER = re.compile(r"## (\d+\.\d+\.\d+) (\(\d{4}-\d{2}-\d{2}\))")
MD_HEADER = re.compile(r"^(#+) (.*)\n\n", re.MULTILINE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--plain-text",
        action="store_true",
        help="Print release message for plain text.",
    )
    parser.add_argument(
        "-g",
        "--github-release",
        action="store_true",
        help="Print release notes for GitHub.",
    )
    args = parser.parse_args()

    changelog = CHANGELOG_PATH.read_text()

    # Retrieve releases notes
    releases = RELEASE_PATTERN.findall(changelog)
    if not releases:
        sys.exit(-1)

    latest_release_content: str = releases.pop(0).strip()

    # Retrieve version
    latest_version_match = VERSION_HEADER.search(latest_release_content)
    if not latest_version_match:
        sys.exit(-1)
    latest_version = latest_version_match.group(1)

    # Format content for plain text
    if args.plain_text:
        # Change markdown title
        content = latest_release_content.replace(
            latest_version_match.group(), f"## Version {latest_version}"
        )
        # Remove bold
        content = content.replace("**", "")
        # Generate sections
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

    # Format content for GitHub release
    elif args.github_release:
        content = latest_release_content.replace(
            latest_version_match.group(), "## What's Changed"
        )
        content += "\n\n---\n\nSee [CHANGELOG.md](./CHANGELOG.md)."

    # Fallback to raw content
    else:
        content = latest_release_content

    content = content.strip()
    if content:
        print(content)
    else:
        sys.exit(-1)
