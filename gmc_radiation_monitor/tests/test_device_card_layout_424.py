from pathlib import Path


def test_connected_device_card_icon_layout_is_consistent() -> None:
    source = Path("rootfs/usr/local/lib/gmc_bridge/report_web.py").read_text(encoding="utf-8")
    assets = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
    assert 'title=t("Connected GMC devices")' in source
    block = source.split("multi_device_html =", 1)[1].split("report_options =", 1)[0]
    assert "Device details, live values and analysis selection are shown below." not in block
    assert 'class="device-card-title"' in source
    assert 'device_visual_class, device_icon = "device-320", "320"' in source
    assert 'device_visual_class, device_icon = "device-500", "500+"' in source
    assert 'class="assessment-icon device-card-icon">{html.escape(device_icon)}</div>' in source
    assert 'class="device-card-title-copy"' in source
    assert ".device-card-title { display:flex;" in assets
