import argparse

from hartware_lib.core.settings.slack import SlackConfig
from hartware_lib.slack.base import SlackHandler


def main():
    parser = argparse.ArgumentParser(description="Slack message sender.")
    parser.add_argument("message", help="set the message")
    parser.add_argument("-c", "--channel", help="set the channel")

    args = parser.parse_args()

    SlackHandler(SlackConfig()).send(
        args.message,
        channel=args.channel,
    )
