from __future__ import annotations

import ast
import json
import sys
import tempfile
import types
from pathlib import Path
from types import SimpleNamespace

try:
    import paho.mqtt.client  # type: ignore[import-not-found]
except ImportError:
    paho = types.ModuleType("paho")
    paho_mqtt = types.ModuleType("paho.mqtt")
    paho_client = types.ModuleType("paho.mqtt.client")
    paho_client.MQTT_ERR_SUCCESS = 0
    paho_mqtt.client = paho_client
    paho.mqtt = paho_mqtt
    sys.modules["paho"] = paho
    sys.modules["paho.mqtt"] = paho_mqtt
    sys.modules["paho.mqtt.client"] = paho_client

from gmc_bridge.device_profiles import DeviceCapabilities
from gmc_bridge.history import HistoryStore
from gmc_bridge.mqtt_pub import MqttPublisher
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import build_report, load_timezone, resolve_period
from gmc_bridge.translations import _TRANSLATIONS, SUPPORTED_UI_LANGUAGES, Translator, validate_catalogs

ROOT = Path(__file__).parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def _static_translation_keys() -> set[str]:
    keys: set[str] = set()
    for filename in (
        "report_web.py",
        "reports.py",
        "mqtt_pub.py",
        "web_components.py",
        "historical_presentation.py",
        "explanations.py",
        "analysis_presentation.py",
    ):
        tree = ast.parse((LIB / filename).read_text(encoding="utf-8"))
        keys.update(
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "t"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        )
    return keys


def _dynamic_ui_keys() -> set[str]:
    tree = ast.parse((LIB / "report_web.py").read_text(encoding="utf-8"))
    keys = {
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "metric_card"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    }
    translated_option_values = {
        "pdf",
        "zip",
        "csv",
        "png",
        "analysis-json",
        "daily-summary-csv",
        "events-csv",
        "histogram-png",
        "heatmap-png",
        "simple",
        "advanced",
    }
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Tuple, ast.List)) or len(node.elts) != 2:
            continue
        if not all(isinstance(item, ast.Constant) and isinstance(item.value, str) for item in node.elts):
            continue
        value, label = (item.value for item in node.elts)
        if value in translated_option_values:
            keys.add(label)
    return keys


def _store(path: Path) -> HistoryStore:
    store = HistoryStore(path)
    store.set_metadata(
        {
            "serial": "device-a",
            "device_model": "GMC-320Re 4.52",
            "device_profile_name": "GMC-300/320 family",
            "app_version": "4.6.2",
        }
    )
    store.upsert_device_registry(
        "device-a",
        {
            "serial": "device-a",
            "device_model": "GMC-320Re 4.52",
            "device_profile_name": "GMC-300/320 family",
            "port": "/dev/ttyUSB0",
            "last_seen_utc": "2026-07-12T10:00:00Z",
        },
    )
    store.set_device_capabilities(
        "device-a", {"cpm": True, "temperature": True, "voltage": True, "gyro": False}
    )
    for index in range(120):
        store.insert_measurement(
            {"cpm": 14, "temperature_c": 24.0, "voltage_v": 4.1},
            device_serial="device-a",
            timestamp_utc=1_783_840_000 + index * 60,
            expected_interval_seconds=60,
        )
    return store


def test_catalogues_have_identical_keys_and_valid_placeholders():
    assert validate_catalogs() == []
    canonical = set(_TRANSLATIONS["en"])
    for language in SUPPORTED_UI_LANGUAGES:
        assert set(_TRANSLATIONS[language]) == canonical


def test_all_runtime_and_dynamic_ui_keys_have_every_translation():
    required = _static_translation_keys() | _dynamic_ui_keys()
    for language in SUPPORTED_UI_LANGUAGES:
        if language == "en":
            continue
        missing = sorted(required - set(_TRANSLATIONS[language]))
        assert missing == [], f"missing {language} translations: {missing}"


def test_all_non_english_dashboards_hide_known_english_runtime_text():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = _store(Path(temp_dir) / "history.sqlite3")
        forbidden = (
            "Timestamp diagnostics",
            "Interval diagnostics",
            "Analysis PDF",
            "Start with a readable PDF",
            "Export details",
            "Restore is disabled by default",
            "Type RESTORE to confirm",
            "Device Profile",
            "Detected Capabilities",
            "Derived from latest CPM",
            "No sustained relative anomaly events detected",
            ">Poor<",
        )
        for language in SUPPORTED_UI_LANGUAGES:
            if language == "en":
                continue
            app = ReportApplication(
                store=store,
                timezone_name="Europe/Berlin",
                scan_interval_seconds=60,
                read_gyro=False,
                cpm_per_usvh=154.0,
                ui_language=language,
            )
            rendered = app.render_index(language_override=language, mode_override="advanced").decode("utf-8")
            for phrase in forbidden:
                assert phrase not in rendered, f"{language} still exposes {phrase!r}"


def test_localized_reports_render_and_machine_schemas_remain_stable():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = _store(Path(temp_dir) / "history.sqlite3")
        tz = load_timezone("Europe/Berlin")
        period = resolve_period(
            kind="daily",
            selection="specific",
            tz=tz,
            date_value="2026-07-12",
        )
        for language in SUPPORTED_UI_LANGUAGES:
            name, content_type, payload = build_report(
                store,
                period=period,
                timezone_name="Europe/Berlin",
                scan_interval_seconds=60,
                output_format="analysis-json",
                device_serial="device-a",
                language=language,
            )
            assert name.endswith("analysis.json")
            assert content_type.startswith("application/json")
            document = json.loads(payload)
            assert document["language"] == language
            assert document["notes"][0] == Translator(language)("CPM is the primary measurement.")

        _, _, csv_payload = build_report(
            store,
            period=period,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            output_format="csv",
            device_serial="device-a",
            language="de",
        )
        assert csv_payload.startswith(
            b"timestamp_utc,timestamp_local,cpm,temperature_c,voltage_v,gyro_x,gyro_y,gyro_z,cpm_quality\n"
        )

        for output_format, signature in (("png", b"\x89PNG"), ("pdf", b"%PDF")):
            _, _, payload = build_report(
                store,
                period=period,
                timezone_name="Europe/Berlin",
                scan_interval_seconds=60,
                output_format=output_format,
                device_serial="device-a",
                language="de",
            )
            assert payload.startswith(signature)


def test_mqtt_discovery_uses_configured_language():
    publisher = MqttPublisher.__new__(MqttPublisher)
    publisher.settings = SimpleNamespace(read_gyro=False, publish_advanced_sensors=True)
    publisher.serial = "device-a"
    publisher.version = "GMC-320Re 4.52"
    publisher.node_id = "gmc_device_a"
    publisher.t = Translator("de")
    publisher.capabilities = DeviceCapabilities(
        cpm=True, temperature=True, voltage=True, gyro=False, gyro_probe_requested=False
    )
    base = "gmc/device-a"
    publisher.state_topic = f"{base}/state"
    publisher.diagnostics_topic = f"{base}/diagnostics"
    publisher.device_availability_topic = f"{base}/device_availability"
    publisher.availability_topics = {
        "cpm": f"{base}/availability",
        "temperature": f"{base}/temperature_availability",
        "voltage": f"{base}/voltage_availability",
        "gyro": f"{base}/gyro_availability",
    }
    messages = dict(publisher._discovery_messages())
    cpm = json.loads(next(value for key, value in messages.items() if key.endswith("/cpm/config")))
    profile = json.loads(
        next(value for key, value in messages.items() if key.endswith("/device_profile/config"))
    )
    assert cpm["name"] == "Strahlung CPM"
    assert cpm["device"]["name"] == "GMC-Strahlungsmonitor"
    assert profile["name"] == "Geräteprofil"


def test_croatian_catalogue_is_complete_and_used_for_mqtt():
    required = set().union(*_TRANSLATIONS.values())
    assert required - set(_TRANSLATIONS["hr"]) == set()
    assert Translator("hr")("Connected GMC devices") == "Povezani GMC uređaji"
    assert Translator("hr")("Radiation CPM") == "CPM zračenja"
    assert Translator("hr")("Home Assistant location") == "Lokacija Home Assistanta"
