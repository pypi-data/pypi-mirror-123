from dataclasses import dataclass
from os import environ
from typing import Optional

from hartware_lib.utils.get_attr import get_or_raise


@dataclass
class SlackConfig:
    TOKEN: str = get_or_raise(
        environ.copy(), "SLACK_BOT_TOKEN", "Slack token must be set"
    )
    DEFAULT_CHANNEL: Optional[str] = environ.get("SLACK_BOT_DEFAULT_CHANNEL")
