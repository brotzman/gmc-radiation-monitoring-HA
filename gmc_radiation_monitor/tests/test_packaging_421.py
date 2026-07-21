from pathlib import Path

import yaml
from PIL import Image

ROOT = Path(__file__).parents[1]


def test_current_version_and_store_description():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    assert config["version"] == "8.4.2"
    assert "background anomaly detection" in config["description"]
    assert config["homeassistant_api"] is True
    assert config["hassio_api"] is True
    assert "hassio_role" not in config
    assert not (ROOT / "rootfs/usr/local/lib/gmc_bridge/supervisor_addon.py").exists()


def test_readme_header_and_location_documentation():
    readme = (ROOT / "README.md").read_text()
    assert readme.startswith("![ ](logo1.png)\n\n# **GMC Radiation Monitor**")
    assert "authenticated internal Core API" in readme
    assert "external geocoding service" in readme
    assert "`hr`" in readme


def test_home_assistant_artwork_is_valid():
    for filename in ("logo.png", "icon.png"):
        with Image.open(ROOT / filename) as image:
            assert image.width == image.height
            assert image.width >= 128
    with Image.open(ROOT / "logo1.png") as image:
        assert image.width > image.height


def test_translated_configuration_names_are_functionally_grouped():
    schema = yaml.safe_load((ROOT / "config.yaml").read_text())["schema"]
    expected_keys = set(schema)
    for path in sorted((ROOT / "translations").glob("*.yaml")):
        configuration = yaml.safe_load(path.read_text())["configuration"]
        assert set(configuration) == expected_keys
        for key, item in configuration.items():
            assert item["name"] and item["description"]
            expected_fields = set(schema[key][0] if isinstance(schema[key], list) else schema[key])
            assert set(item["fields"]) == expected_fields
            assert all(field["name"] and field["description"] for field in item["fields"].values())
