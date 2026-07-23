from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Protocol, runtime_checkable

from .history import HistoryRow


@runtime_checkable
class HistoryReader(Protocol):
    """Stable read-only interface used by analysis and presentation modules."""

    def query_range(
        self,
        start_utc: int,
        end_utc: int,
        *,
        device_serial: str | None = None,
    ) -> list[HistoryRow]: ...

    def bounds(self, *, device_serial: str | None = None) -> tuple[int | None, int | None]: ...


@runtime_checkable
class DeviceRegistryReader(Protocol):
    def list_device_registry(self) -> list[dict[str, Any]]: ...


@runtime_checkable
class TranslatorLike(Protocol):
    language: str

    def __call__(self, key: str, /, **values: Any) -> str: ...


@runtime_checkable
class LiveMeasurementProvider(Protocol):
    def live_devices_payload(self, *, language: str) -> Mapping[str, Any]: ...


@runtime_checkable
class DiagnosticProvider(Protocol):
    def snapshot(self) -> Mapping[str, Any]: ...


@runtime_checkable
class MeasurementSink(Protocol):
    def add_measurements(self, rows: Iterable[HistoryRow]) -> None: ...
