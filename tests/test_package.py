"""Basic package test."""


def test_package_import() -> None:
    """Import package."""
    import pffmpeg  # noqa: F401, PLC0415


def test_package_version_is_defined() -> None:
    """Check imported package have __version__ defined."""
    import pffmpeg  # noqa: PLC0415

    assert pffmpeg.__version__ != "undefined"
