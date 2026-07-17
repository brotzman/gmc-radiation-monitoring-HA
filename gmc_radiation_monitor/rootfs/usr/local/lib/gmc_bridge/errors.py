class GmcError(Exception):
    """Base class for device communication errors."""


class GmcTimeout(GmcError):
    """Raised when an exact response does not arrive in time."""


class GmcProtocolError(GmcError):
    """Raised when a response violates expected framing."""


class DeviceBusy(GmcError):
    """Raised when another process already owns the serial device."""


class DeviceIdentityChanged(GmcProtocolError):
    """Raised when a different physical GMC appears after reconnect."""


class MqttError(Exception):
    """Raised for MQTT publish failures that must not crash serial polling."""


def classify_optional_issue(sensor: str, exc: BaseException):
    """Map technical optional-channel failures to a stable user-facing issue code."""
    from .presentation_models import AnalysisStatus, DeviceIssue

    code = {
        "gyro": "orientation_frame_invalid" if isinstance(exc, GmcProtocolError) else "orientation_unavailable",
        "temperature": "temperature_unavailable",
        "voltage": "voltage_unavailable",
        "device_time": "device_time_unavailable",
        "dual_tube": "tube_data_unavailable",
    }.get(sensor, "optional_channel_unavailable")
    return DeviceIssue(
        code=code,
        severity=AnalysisStatus.NOTICE,
        affects_measurement=False,
        retryable=True,
        technical_detail=str(exc),
        values={"sensor": sensor},
    )
