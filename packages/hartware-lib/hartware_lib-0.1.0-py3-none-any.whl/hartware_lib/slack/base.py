import logging
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

from hartware_lib.slack.exceptions import ApiError, ChannelMustBeSet

logger = logging.getLogger(__name__)


class SlackHandler:
    def __init__(self, config):
        self.config = config
        self.client = WebClient(token=self.config.TOKEN)

    def send(self, msg: str, channel: Optional[str] = None) -> SlackResponse:
        if not channel and self.config.DEFAULT_CHANNEL:
            channel = self.config.DEFAULT_CHANNEL

        elif not channel:
            channel_error = ChannelMustBeSet()
            logger.warning(channel_error.message)

            raise channel_error

        try:
            return self.client.chat_postMessage(channel=channel, text=msg)
        except SlackApiError:
            api_error = ApiError()
            logger.warning(api_error.message)
            raise api_error
