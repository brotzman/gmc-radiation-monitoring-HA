#!/usr/bin/env python3
"""GQ GMC to MQTT bridge launcher."""
from __future__ import annotations

import sys
from pathlib import Path

# In the Home Assistant image /usr/local/lib is already importable. During repository tests,
# add the adjacent source tree explicitly so the same launcher remains directly testable.
LIB_DIR = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge import (  # noqa: E402,F401
    DeviceBusy,
    DeviceIdentityChanged,
    GmcError,
    GmcProtocolError,
    GmcTimeout,
    HighCpmGate,
    MqttError,
    OptionalReadError,
    SampleResult,
    SerialGmc,
    Settings,
    ensure_same_serial,
    parse_bool,
    read_identity,
    read_sample,
    slugify,
    utc_timestamp,
)
from gmc_bridge.mqtt_pub import (  # noqa: E402,F401
    MQTT_MAX_INFLIGHT_MESSAGES,
    MQTT_MAX_QUEUED_MESSAGES,
    MQTT_PUBLISH_TIMEOUT,
    MqttPublisher,
)
from gmc_bridge.service import STOP_EVENT, configure_logging, format_published_sample, main  # noqa: E402,F401

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        configure_logging()
        import logging

        logging.getLogger("gmc_bridge").exception("Fatal error: %s", exc)
        raise SystemExit(1) from None
