from pathlib import Path

from gmc_bridge.version import APP_VERSION


def test_release_691_version_and_notes_are_packaged() -> None:
    root = Path(__file__).parents[1]
    assert APP_VERSION == "8.0.13"
    assert (root / "RELEASE_NOTES_8.0.13.md").is_file()
    assert "Verify every RFC1801" in (root / "CHANGELOG.md").read_text()
