from __future__ import annotations

import fnmatch
import json
import math
import os
import threading
import time
from dataclasses import asdict, dataclass
from datetime import UTC
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .version import USER_AGENT


@dataclass(frozen=True)
class HomeAssistantLocation:
    available: bool
    location_name: str = ""
    latitude: float | None = None
    longitude: float | None = None
    elevation: int | float | None = None
    country: str = ""
    time_zone: str = ""
    error: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HomeAssistantTemperature:
    available: bool
    temperature_c: float | None = None
    entity_id: str = ""
    friendly_name: str = ""
    age_seconds: float | None = None
    error: str = ""


class HomeAssistantTemperatureClient:
    """Read and cache one Home Assistant temperature entity."""

    def __init__(
        self,
        *,
        entity_id: str = "",
        friendly_name: str = "",
        token: str | None = None,
        cache_seconds: int = 30,
        timeout_seconds: float = 3.0,
        max_age_seconds: int = 900,
    ) -> None:
        self.entity_id = entity_id.strip()
        self.friendly_name = friendly_name.strip()
        self.token = token if token is not None else os.environ.get("SUPERVISOR_TOKEN", "")
        self.cache_seconds = max(5, int(cache_seconds))
        self.timeout_seconds = max(0.5, float(timeout_seconds))
        self.max_age_seconds = max(30, int(max_age_seconds))
        self._lock = threading.Lock()
        self._cached: HomeAssistantTemperature | None = None
        self._cached_at = 0.0

    def get_temperature(self) -> HomeAssistantTemperature:
        now = time.monotonic()
        with self._lock:
            if self._cached is not None and now - self._cached_at < self.cache_seconds:
                return self._cached
            result = self._fetch_temperature()
            self._cached = result
            self._cached_at = now
            return result

    def _request_json(self, endpoint: str) -> object:
        request = Request(
            endpoint,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="GET",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - fixed internal HA URL
            if response.status != 200:
                raise OSError(f"Home Assistant API returned HTTP {response.status}")
            return json.load(response)

    def _fetch_temperature(self) -> HomeAssistantTemperature:
        if not self.token:
            return HomeAssistantTemperature(False, error="Home Assistant API token is unavailable")
        try:
            candidates: list[object]
            if self.entity_id:
                try:
                    payload = self._request_json(
                        "http://supervisor/core/api/states/" + quote(self.entity_id, safe="")
                    )
                    candidates = [payload]
                except HTTPError as exc:
                    if exc.code != 404 or not self.friendly_name:
                        raise
                    payload = self._request_json("http://supervisor/core/api/states")
                    candidates = payload if isinstance(payload, list) else []
            else:
                payload = self._request_json("http://supervisor/core/api/states")
                candidates = payload if isinstance(payload, list) else []
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            return HomeAssistantTemperature(False, error=str(exc))

        wanted = self.friendly_name.casefold()
        selected: dict[str, Any] | None = None
        for item in candidates:
            if not isinstance(item, dict):
                continue
            attrs = item.get("attributes") if isinstance(item.get("attributes"), dict) else {}
            name = str(attrs.get("friendly_name") or "").strip()
            device_class = str(attrs.get("device_class") or "").strip()
            entity_id = str(item.get("entity_id") or "").strip()
            if self.entity_id and entity_id == self.entity_id:
                selected = item
                break
            if wanted and wanted in name.casefold() and device_class == "temperature":
                selected = item
                break
        if selected is None:
            target = self.entity_id or self.friendly_name or "configured temperature sensor"
            return HomeAssistantTemperature(False, error=f"Temperature entity not found: {target}")

        attrs = selected.get("attributes") if isinstance(selected.get("attributes"), dict) else {}
        try:
            value = float(selected.get("state"))
        except (TypeError, ValueError):
            return HomeAssistantTemperature(False, error="Temperature entity state is not numeric")
        if not math.isfinite(value):
            return HomeAssistantTemperature(False, error="Temperature entity state is not finite")
        unit = str(attrs.get("unit_of_measurement") or "°C").strip().upper()
        if unit in {"°F", "F", "DEG F", "DEGF"}:
            value = (value - 32.0) * 5.0 / 9.0
        elif unit not in {"°C", "C", "DEG C", "DEGC"}:
            return HomeAssistantTemperature(False, error=f"Unsupported temperature unit: {unit}")

        age_seconds = None
        updated = str(selected.get("last_updated") or selected.get("last_changed") or "")
        if updated:
            try:
                from datetime import datetime

                stamp = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                age_seconds = max(0.0, (datetime.now(UTC) - stamp).total_seconds())
            except (TypeError, ValueError):
                age_seconds = None
        stale_error = ""
        if age_seconds is not None and age_seconds > self.max_age_seconds:
            stale_error = "Temperature entity state is stale"
        return HomeAssistantTemperature(
            True,
            round(value, 3),
            str(selected.get("entity_id") or ""),
            str(attrs.get("friendly_name") or ""),
            age_seconds,
            stale_error,
        )


@dataclass(frozen=True)
class HomeAssistantPressureSource:
    available: bool
    entity_id: str = ""
    friendly_name: str = ""
    pressure_hpa: float | None = None
    age_seconds: float | None = None
    unit: str = ""
    error: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HomeAssistantPressure:
    available: bool
    pressure_hpa: float | None = None
    provider_name: str = ""
    source_mode: str = "unavailable"
    source_count: int = 0
    source_spread_hpa: float | None = None
    sources: tuple[HomeAssistantPressureSource, ...] = ()
    error: str = ""

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["sources"] = [source.as_dict() for source in self.sources]
        return payload


class HomeAssistantPressureClient:
    """Read, validate and cache pressure from one or two HA weather entities.

    Weather entities expose their condition as the state and pressure as an
    attribute.  When two current sources agree, their mean is used as a
    plausibilised site pressure.  Disagreeing sources are rejected rather than
    silently selecting the value that best fits the radiation data.
    """

    def __init__(
        self,
        *,
        entity_ids: tuple[str, ...] | list[str],
        provider_name: str = "",
        token: str | None = None,
        cache_seconds: int = 60,
        timeout_seconds: float = 3.0,
        max_age_seconds: int = 7200,
        max_difference_hpa: float = 5.0,
    ) -> None:
        self.entity_ids = tuple(
            dict.fromkeys(str(value).strip() for value in entity_ids if str(value).strip())
        )
        self.provider_name = provider_name.strip()
        self.token = token if token is not None else os.environ.get("SUPERVISOR_TOKEN", "")
        self.cache_seconds = max(10, int(cache_seconds))
        self.timeout_seconds = max(0.5, float(timeout_seconds))
        self.max_age_seconds = max(60, int(max_age_seconds))
        self.max_difference_hpa = max(0.1, float(max_difference_hpa))
        self._lock = threading.Lock()
        self._cached: HomeAssistantPressure | None = None
        self._cached_at = 0.0

    def get_pressure(self) -> HomeAssistantPressure:
        now = time.monotonic()
        with self._lock:
            if self._cached is not None and now - self._cached_at < self.cache_seconds:
                return self._cached
            result = self._fetch_pressure()
            self._cached = result
            self._cached_at = now
            return result

    def _request_states(self) -> object:
        request = Request(
            "http://supervisor/core/api/states",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="GET",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - fixed internal HA URL
            if response.status != 200:
                raise OSError(f"Home Assistant API returned HTTP {response.status}")
            return json.load(response)

    def _find_state_fallback(self, entity_id: str) -> object:
        payload = self._request_states()
        if not isinstance(payload, list):
            raise ValueError("Invalid Home Assistant states response")
        requested = entity_id.strip().casefold()
        if not requested:
            raise ValueError("No weather entity id configured")

        def _friendly_name(item: dict[str, Any]) -> str:
            attrs = item.get("attributes") if isinstance(item.get("attributes"), dict) else {}
            return str(attrs.get("friendly_name") or "").strip()

        exact: dict[str, Any] | None = None
        alias: dict[str, Any] | None = None
        requested_suffix = requested.split(".", 1)[-1]
        for item in payload:
            if not isinstance(item, dict):
                continue
            candidate = str(item.get("entity_id") or "").strip()
            if not candidate.startswith("weather."):
                continue
            attrs = item.get("attributes") if isinstance(item.get("attributes"), dict) else {}
            if attrs.get("pressure") is None and attrs.get("native_pressure") is None:
                continue
            candidate_cf = candidate.casefold()
            if candidate_cf == requested:
                exact = item
                break
            if candidate_cf.startswith(requested):
                alias = alias or item
                continue
            suffix = candidate_cf.split(".", 1)[-1]
            if suffix == requested_suffix or suffix.startswith(requested_suffix + "_"):
                alias = alias or item
                continue
            friendly = _friendly_name(item).casefold().replace("forecast ", "").strip()
            if requested_suffix.startswith("forecast_"):
                wanted = requested_suffix.removeprefix("forecast_").replace("_", " ").strip()
                if wanted and wanted in friendly:
                    alias = alias or item
        if exact is not None:
            return exact
        if alias is not None:
            return alias
        raise ValueError(f"Weather entity not found: {entity_id}")

    def _request_state(self, entity_id: str) -> object:
        request = Request(
            "http://supervisor/core/api/states/" + quote(entity_id, safe=""),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="GET",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - fixed internal HA URL
            if response.status != 200:
                raise OSError(f"Home Assistant API returned HTTP {response.status}")
            return json.load(response)

    @staticmethod
    def _age_seconds(payload: dict[str, Any]) -> float | None:
        updated = str(payload.get("last_updated") or payload.get("last_changed") or "")
        if not updated:
            return None
        try:
            from datetime import datetime

            stamp = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            return max(0.0, (datetime.now(UTC) - stamp).total_seconds())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_hpa(value: object, unit: object) -> float:
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError("Pressure value is not finite")
        normalized = str(unit or "hPa").strip().lower().replace(" ", "").replace("_", "")
        normalized = normalized.replace("″", "in").replace('"', "in")
        if normalized in {"hpa", "mbar", "mb", "hectopascal", "hectopascals"}:
            result = numeric
        elif normalized in {"pa", "pascal", "pascals"}:
            result = numeric / 100.0
        elif normalized in {"kpa", "kilopascal", "kilopascals"}:
            result = numeric * 10.0
        elif normalized in {"bar", "bars"}:
            result = numeric * 1000.0
        elif normalized in {"inhg", "inmercury"}:
            result = numeric * 33.8638866667
        elif normalized in {"mmhg", "torr"}:
            result = numeric * 1.33322387415
        elif normalized in {"psi"}:
            result = numeric * 68.9475729
        else:
            raise ValueError(f"Unsupported pressure unit: {unit}")
        if not 750.0 <= result <= 1150.0:
            raise ValueError(f"Pressure value outside plausible weather range: {result:.1f} hPa")
        return result

    def _read_source(self, entity_id: str) -> HomeAssistantPressureSource:
        try:
            try:
                payload = self._request_state(entity_id)
            except HTTPError as exc:
                if exc.code != 404:
                    raise
                payload = self._find_state_fallback(entity_id)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            return HomeAssistantPressureSource(False, entity_id=entity_id, error=str(exc))
        if not isinstance(payload, dict):
            return HomeAssistantPressureSource(
                False, entity_id=entity_id, error="Invalid Home Assistant state response"
            )
        attrs = payload.get("attributes") if isinstance(payload.get("attributes"), dict) else {}
        friendly_name = str(attrs.get("friendly_name") or entity_id).strip()
        value = attrs.get("pressure", attrs.get("native_pressure"))
        unit = attrs.get(
            "pressure_unit", attrs.get("native_pressure_unit", attrs.get("unit_of_measurement", "hPa"))
        )
        if value is None:
            return HomeAssistantPressureSource(
                False,
                entity_id=entity_id,
                friendly_name=friendly_name,
                unit=str(unit or ""),
                error="Weather entity does not provide a pressure attribute",
            )
        try:
            pressure_hpa = self._to_hpa(value, unit)
        except (TypeError, ValueError) as exc:
            return HomeAssistantPressureSource(
                False, entity_id=entity_id, friendly_name=friendly_name, unit=str(unit or ""), error=str(exc)
            )
        age_seconds = self._age_seconds(payload)
        if age_seconds is not None and age_seconds > self.max_age_seconds:
            return HomeAssistantPressureSource(
                False,
                entity_id=entity_id,
                friendly_name=friendly_name,
                pressure_hpa=round(pressure_hpa, 3),
                age_seconds=age_seconds,
                unit=str(unit or ""),
                error="Weather pressure state is stale",
            )
        return HomeAssistantPressureSource(
            True,
            entity_id=entity_id,
            friendly_name=friendly_name,
            pressure_hpa=round(pressure_hpa, 3),
            age_seconds=age_seconds,
            unit=str(unit or ""),
            error="",
        )

    def _fetch_pressure(self) -> HomeAssistantPressure:
        if not self.entity_ids:
            return HomeAssistantPressure(
                False, provider_name=self.provider_name, error="No weather pressure entity is configured"
            )
        if not self.token:
            return HomeAssistantPressure(
                False, provider_name=self.provider_name, error="Home Assistant API token is unavailable"
            )
        sources = tuple(self._read_source(entity_id) for entity_id in self.entity_ids)
        valid = [source for source in sources if source.available and source.pressure_hpa is not None]
        if not valid:
            errors = "; ".join(source.error for source in sources if source.error)
            return HomeAssistantPressure(
                False,
                provider_name=self.provider_name,
                sources=sources,
                error=errors or "No current pressure source is available",
            )
        values = [float(source.pressure_hpa) for source in valid]
        spread = max(values) - min(values) if len(values) > 1 else 0.0
        if len(values) > 1 and spread > self.max_difference_hpa:
            return HomeAssistantPressure(
                False,
                provider_name=self.provider_name,
                source_mode="disagreement",
                source_count=len(valid),
                source_spread_hpa=round(spread, 3),
                sources=sources,
                error=f"Weather pressure sources disagree by {spread:.1f} hPa",
            )
        pressure_hpa = sum(values) / len(values)
        return HomeAssistantPressure(
            True,
            pressure_hpa=round(pressure_hpa, 3),
            provider_name=self.provider_name,
            source_mode="plausibilized" if len(values) > 1 else "single",
            source_count=len(valid),
            source_spread_hpa=round(spread, 3),
            sources=sources,
            error="",
        )


class HomeAssistantConfigClient:
    """Read and cache the configured Home Assistant instance location.

    The client only uses Home Assistant's internal Core API proxy. It does not
    reverse-geocode coordinates or transmit them to any external service.
    """

    def __init__(
        self,
        *,
        endpoint: str = "http://supervisor/core/api/config",
        token: str | None = None,
        cache_seconds: int = 300,
        timeout_seconds: float = 3.0,
    ) -> None:
        self.endpoint = endpoint
        self.token = token if token is not None else os.environ.get("SUPERVISOR_TOKEN", "")
        self.cache_seconds = max(30, int(cache_seconds))
        self.timeout_seconds = max(0.5, float(timeout_seconds))
        self._lock = threading.Lock()
        self._cached: HomeAssistantLocation | None = None
        self._cached_at = 0.0

    def get_location(self) -> HomeAssistantLocation:
        now = time.monotonic()
        with self._lock:
            if self._cached is not None and now - self._cached_at < self.cache_seconds:
                return self._cached

            location = self._fetch_location()
            self._cached = location
            self._cached_at = now
            return location

    def _fetch_location(self) -> HomeAssistantLocation:
        if not self.token:
            return HomeAssistantLocation(
                available=False,
                error="Home Assistant API token is unavailable",
            )

        request = Request(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - fixed internal Home Assistant URL
                if response.status != 200:
                    return HomeAssistantLocation(
                        available=False,
                        error=f"Home Assistant API returned HTTP {response.status}",
                    )
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            return HomeAssistantLocation(available=False, error=str(exc))

        if not isinstance(payload, dict):
            return HomeAssistantLocation(available=False, error="Invalid Home Assistant config response")

        latitude = self._finite_float(payload.get("latitude"))
        longitude = self._finite_float(payload.get("longitude"))
        elevation = self._finite_float(payload.get("elevation"))
        location_name = str(payload.get("location_name") or "").strip()
        country = str(payload.get("country") or "").strip().upper()
        time_zone = str(payload.get("time_zone") or "").strip()

        if not location_name and (latitude is None or longitude is None):
            return HomeAssistantLocation(
                available=False,
                error="Home Assistant location is not configured",
            )

        if elevation is not None and elevation.is_integer():
            elevation = int(elevation)

        return HomeAssistantLocation(
            available=True,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            elevation=elevation,
            country=country,
            time_zone=time_zone,
        )

    def create_persistent_notification(
        self,
        *,
        title: str,
        message: str,
        notification_id: str,
    ) -> None:
        """Create or update one Home Assistant persistent notification."""
        if not self.token:
            raise OSError("Home Assistant API token is unavailable")
        safe_id = "".join(
            character for character in str(notification_id) if character.isalnum() or character in "_-"
        )[:80]
        if not safe_id:
            raise ValueError("A notification id is required")
        endpoint = "http://supervisor/core/api/services/persistent_notification/create"
        body = json.dumps(
            {
                "title": str(title)[:200],
                "message": str(message)[:4000],
                "notification_id": safe_id,
            }
        ).encode("utf-8")
        request = Request(
            endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="POST",
        )
        with urlopen(request, timeout=max(5.0, self.timeout_seconds)) as response:  # nosec B310 - fixed internal HA URL
            if response.status not in {200, 201}:
                raise OSError(f"Home Assistant API returned HTTP {response.status}")

    def purge_recorder_entity_globs(
        self, entity_globs: list[str], serials: list[str] | None = None
    ) -> dict[str, Any]:
        """Delete Recorder states and statistics for every actual GMC entity.

        Entity IDs are user-editable in Home Assistant, so serial-derived globs alone are
        insufficient. Resolve registry entries by their immutable MQTT unique_id first,
        then submit the exact entity IDs as well as legacy globs.
        """
        globs = sorted({str(item).strip() for item in entity_globs if str(item).strip()})
        serial_values = sorted({str(item).strip() for item in (serials or []) if str(item).strip()})
        if not globs and not serial_values:
            raise ValueError("No Home Assistant GMC entities were supplied")
        if not self.token:
            raise OSError("Home Assistant API token is unavailable")

        entity_ids = self._resolve_gmc_entity_ids(serial_values, globs)
        if not entity_ids and not globs:
            raise OSError("No Home Assistant GMC entities were found")

        endpoint = "http://supervisor/core/api/services/recorder/purge_entities"
        request_data: dict[str, Any] = {"keep_days": 0}
        if entity_ids:
            request_data["entity_id"] = entity_ids
        if globs:
            request_data["entity_globs"] = globs
        body = json.dumps(request_data).encode("utf-8")
        request = Request(
            endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="POST",
        )
        with urlopen(request, timeout=max(10.0, self.timeout_seconds)) as response:  # nosec B310
            if response.status not in {200, 201}:
                raise OSError(f"Home Assistant API returned HTTP {response.status}")
            payload = json.load(response)

        statistic_ids = self._clear_recorder_statistics(entity_ids, globs)
        return {
            "entity_ids": entity_ids,
            "entity_globs": globs,
            "statistic_ids": statistic_ids,
            "response": payload,
        }

    def _authenticated_websocket(self):
        try:
            from websockets.sync.client import connect
        except ImportError as exc:
            raise OSError("Python websockets support is unavailable") from exc
        ws = connect(
            "ws://supervisor/core/websocket",
            open_timeout=max(10.0, self.timeout_seconds),
            close_timeout=5,
        )
        hello = json.loads(ws.recv())
        if hello.get("type") != "auth_required":
            ws.close()
            raise OSError("Unexpected Home Assistant WebSocket greeting")
        ws.send(json.dumps({"type": "auth", "access_token": self.token}))
        auth = json.loads(ws.recv())
        if auth.get("type") != "auth_ok":
            ws.close()
            raise OSError("Home Assistant WebSocket authentication failed")
        return ws

    def _resolve_gmc_entity_ids(self, serials: list[str], entity_globs: list[str]) -> list[str]:
        """Resolve renamed GMC entities through immutable MQTT unique IDs."""
        from .utils import slugify

        unique_prefixes = tuple(f"gmc_{slugify(serial)}_" for serial in serials)
        entity_ids: set[str] = set()
        ws = self._authenticated_websocket()
        try:
            # The full registry response contains unique_id, unlike the display-optimized list.
            ws.send(json.dumps({"id": 1, "type": "config/entity_registry/list"}))
            response = json.loads(ws.recv())
            if not response.get("success"):
                raise OSError("Unable to list Home Assistant entity registry")
            for item in response.get("result") or []:
                if not isinstance(item, dict):
                    continue
                entity_id = str(item.get("entity_id") or "").strip()
                unique_id = str(item.get("unique_id") or "").strip()
                platform = str(item.get("platform") or "").strip()
                if (
                    entity_id
                    and platform == "mqtt"
                    and unique_prefixes
                    and unique_id.startswith(unique_prefixes)
                ):
                    entity_ids.add(entity_id)
        finally:
            ws.close()

        # Preserve support for installations whose registry endpoint omits older entries.
        try:
            request = Request(
                "http://supervisor/core/api/states",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json",
                    "User-Agent": USER_AGENT,
                },
                method="GET",
            )
            with urlopen(request, timeout=max(10.0, self.timeout_seconds)) as response:  # nosec B310
                states = json.load(response)
            for item in states if isinstance(states, list) else []:
                entity_id = str((item or {}).get("entity_id") or "").strip()
                if entity_id and any(fnmatch.fnmatchcase(entity_id, pattern) for pattern in entity_globs):
                    entity_ids.add(entity_id)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
            pass
        return sorted(entity_ids)

    def _clear_recorder_statistics(self, entity_ids: list[str], entity_globs: list[str]) -> list[str]:
        """Clear HA short- and long-term statistics for exact and legacy GMC IDs."""
        ws = self._authenticated_websocket()
        try:
            ws.send(json.dumps({"id": 1, "type": "recorder/list_statistic_ids"}))
            listed = json.loads(ws.recv())
            if not listed.get("success"):
                raise OSError("Unable to list Home Assistant statistics")
            exact = set(entity_ids)
            ids = sorted(
                {
                    str(item.get("statistic_id") or "")
                    for item in (listed.get("result") or [])
                    if str(item.get("statistic_id") or "") in exact
                    or any(
                        fnmatch.fnmatchcase(str(item.get("statistic_id") or ""), pattern)
                        for pattern in entity_globs
                    )
                }
            )
            if ids:
                ws.send(json.dumps({"id": 2, "type": "recorder/clear_statistics", "statistic_ids": ids}))
                cleared = json.loads(ws.recv())
                if not cleared.get("success"):
                    raise OSError("Unable to clear Home Assistant statistics")
            return ids
        finally:
            ws.close()

    @staticmethod
    def _finite_float(value: object) -> float | None:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return number if math.isfinite(number) else None
