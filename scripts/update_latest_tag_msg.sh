#!/bin/bash
# Update annotated tag on current commit, edit message with release notes.

set -e

MSG=$(./scripts/get_latest_release_notes.py --tag-msg)
TAG=$(git describe --exact-match --tags --abbrev=0)

git tag -f -a $TAG -m "$MSG" > /dev/null
