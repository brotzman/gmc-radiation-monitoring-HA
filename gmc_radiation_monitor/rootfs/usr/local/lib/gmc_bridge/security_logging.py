from __future__ import annotations

import logging
import os
import re
from collections.abc import Iterable

_REDACTED = "[REDACTED]"
_BEARER_PATTERN = re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+")
_CREDENTIAL_PATTERN = re.compile(
    r"(?i)(password|passwd|token|secret|authorization|account[_ -]?id|counter[_ -]?id)"
    r"([\"'=: ]+)([^\s,;\"'}]+)"
)


def sensitive_values_from_environment(extra_values: Iterable[str] = ()) -> tuple[str, ...]:
    names = (
        "MQTT_PASSWORD",
        "SUPERVISOR_TOKEN",
        "GMCMAP_ACCOUNT_ID",
        "GMCMAP_DEVICE_IDS",
    )
    values = [str(os.environ.get(name, "")).strip() for name in names]
    values.extend(str(value).strip() for value in extra_values)
    return tuple(sorted({value for value in values if len(value) >= 4}, key=len, reverse=True))


def redact_text(text: object, *, sensitive_values: Iterable[str] = ()) -> str:
    result = str(text)
    for value in sensitive_values:
        if value:
            result = result.replace(value, _REDACTED)
    result = _BEARER_PATTERN.sub(r"\1" + _REDACTED, result)
    result = _CREDENTIAL_PATTERN.sub(lambda match: match.group(1) + match.group(2) + _REDACTED, result)
    return result


class SecretRedactingFormatter(logging.Formatter):
    """Redact the fully formatted record, including exception tracebacks."""

    def __init__(self, format_string: str, sensitive_values: Iterable[str] = ()) -> None:
        super().__init__(format_string)
        self.sensitive_values = tuple(sensitive_values)

    def format(self, record: logging.LogRecord) -> str:
        rendered = super().format(record)
        return redact_text(rendered, sensitive_values=self.sensitive_values)


class SecretRedactionFilter(logging.Filter):
    def __init__(self, sensitive_values: Iterable[str] = ()) -> None:
        super().__init__()
        self.sensitive_values = tuple(sensitive_values)

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            rendered = record.getMessage()
        except Exception:
            rendered = str(record.msg)
        record.msg = redact_text(rendered, sensitive_values=self.sensitive_values)
        record.args = ()
        return True


def configure_secure_logging(*, level: int, format_string: str) -> None:
    """Configure root logging once and attach secret redaction to every handler."""
    logging.basicConfig(level=level, format=format_string)
    values = sensitive_values_from_environment()
    root = logging.getLogger()
    for handler in root.handlers:
        # The filter protects record consumers; the formatter also redacts
        # exception text and tracebacks produced after filters have run.
        if not any(isinstance(item, SecretRedactionFilter) for item in handler.filters):
            handler.addFilter(SecretRedactionFilter(values))
        handler.setFormatter(SecretRedactingFormatter(format_string, values))
