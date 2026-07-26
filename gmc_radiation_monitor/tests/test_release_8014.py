from pathlib import Path

import yaml

APP_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_ROOT.parent


def test_official_home_assistant_repository_layout() -> None:
    assert APP_ROOT.name == "gmc_radiation_monitor"
    assert (REPO_ROOT / "repository.yaml").is_file()
    assert not (APP_ROOT / "repository.yaml").exists()
    assert not (REPO_ROOT / "config.yaml").exists()

    repository = yaml.safe_load((REPO_ROOT / "repository.yaml").read_text(encoding="utf-8"))
    assert repository == {
        "name": "GMC Radiation Monitor",
        "url": "https://github.com/brotzman/gmc-homeassistant",
        "maintainer": "Brotzman",
    }


def test_app_metadata_uses_official_source_build_distribution() -> None:
    config = yaml.safe_load((APP_ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert config["version"] == "9.3.0"
    assert config["slug"] == "gmc_radiation_monitor"
    assert config["url"] == (
        "https://github.com/brotzman/gmc-homeassistant/tree/main/gmc_radiation_monitor"
    )
    assert "image" not in config
    assert config["arch"] == ["aarch64", "amd64"]
    assert config["ingress"] is True
    assert config["uart"] is True
    assert config["apparmor"] is True
    assert config["panel_icon"] == "mdi:radioactive"


def test_home_assistant_app_files_are_complete() -> None:
    required = {
        "CHANGELOG.md",
        "DOCS.md",
        "Dockerfile",
        "README.md",
        "RELEASE_NOTES_9.3.0.md",
        "apparmor.txt",
        "config.yaml",
        "icon.png",
        "logo.png",
        "rootfs",
        "translations",
    }
    assert required <= {path.name for path in APP_ROOT.iterdir()}
    assert len(list((APP_ROOT / "translations").glob("*.yaml"))) == 8


def test_official_lint_and_multiarch_source_build_workflows_are_at_repository_root() -> None:
    workflows = REPO_ROOT / ".github" / "workflows"
    for filename in ("builder.yaml", "lint.yaml", "quality.yml"):
        assert (workflows / filename).is_file()

    lint = (workflows / "lint.yaml").read_text(encoding="utf-8")
    assert "home-assistant/actions/helpers/find-addons@master" in lint
    assert "frenck/action-addon-linter@v2.21" in lint

    builder = (workflows / "builder.yaml").read_text(encoding="utf-8")
    assert "docker/build-push-action@v6" in builder
    assert "platform: linux/amd64" in builder
    assert "platform: linux/arm64" in builder
    assert "push: false" in builder
    assert "packages: write" not in builder
    assert not (workflows / "build-app.yaml").exists()


def test_repository_documents_explain_app_not_custom_component() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Home Assistant App Repository" in readme
    assert "custom_components" in readme
    assert "MQTT Discovery" in readme
    assert (REPO_ROOT / "SECURITY.md").is_file()
    assert (REPO_ROOT / "CONTRIBUTING.md").is_file()
