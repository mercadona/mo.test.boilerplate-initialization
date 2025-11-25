import os

UNLEASH_ENABLED: bool = os.getenv("UNLEASH_ENABLED", "true").lower() == "true"
UNLEASH_URL: str = os.getenv("UNLEASH_URL", "http://unleash-edge.prod.monline/api/")
UNLEASH_TOKEN: str | None = os.getenv("UNLEASH_TOKEN")
UNLEASH_APP_NAME: str = os.getenv("UNLEASH_APP_NAME", os.environ["APPLICATION_NAME"])
