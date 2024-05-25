"""Basic package test."""


def test_package_import():
    """Import package."""
    import pffmpeg  # noqa: F401


def test_package_version_is_defined():
    """Check imported package have __version__ defined."""
    import pffmpeg

    assert pffmpeg.__version__ != "undefined"
