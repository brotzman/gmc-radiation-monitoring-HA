from __future__ import annotations

from .translations import Translator


def localized_exception_message(t: Translator, exc: BaseException) -> str:
    """Return a localized, user-safe message while preserving full details in logs."""
    message = str(exc).strip()
    translated = t(message)
    if translated != message:
        return translated
    prefix_templates = (
        ("Unknown IANA timezone: ", "Unknown IANA timezone: {value}"),
        ("Unsupported daily selection: ", "Unsupported daily selection: {value}"),
        ("Unsupported weekly selection: ", "Unsupported weekly selection: {value}"),
        ("Unsupported report period: ", "Unsupported report period: {value}"),
        ("Unsupported report format: ", "Unsupported report format: {value}"),
    )
    for prefix, template in prefix_templates:
        if message.startswith(prefix):
            return t(template, value=message[len(prefix) :])
    if message.startswith("Exactly one ") or message.startswith("At most one "):
        return t("Invalid request parameters")
    return t("The request could not be processed. Check the selected options.")
