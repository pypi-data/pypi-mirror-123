from dataclasses import dataclass
from os import environ


@dataclass
class AppConfig:
    TEST: bool = environ.get("TEST", "").lower() in ("1", "y", "yes", "true")
    DEBUG: bool = environ.get("DEBUG", "").lower() in ("1", "y", "yes", "true")
