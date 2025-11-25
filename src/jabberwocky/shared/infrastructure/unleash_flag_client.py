import logging
from typing import Any

from UnleashClient import UnleashClient

from jabberwocky import settings
from jabberwocky.shared.domain.flag_client import Flag, FlagClient

_unleash_client = UnleashClient(
    url=settings.UNLEASH_URL,
    custom_options={"verify": False},
    app_name=settings.UNLEASH_APP_NAME,
    custom_headers={"Authorization": settings.UNLEASH_TOKEN},
    verbose_log_level=logging.CRITICAL,
)

if settings.UNLEASH_ENABLED:
    _unleash_client.initialize_client()


class UnleashFlagClient(FlagClient):
    def is_active(self, flag: Flag) -> bool:
        context: dict[str, Any] = {}
        return _unleash_client.is_enabled(flag.value, context)
