class SlackException(Exception):
    def __init__(self):
        super().__init__(self.message)


class ChannelMustBeSet(SlackException):
    message = "Channel must be set"


class ApiError(SlackException):
    message = "Slack Api error"
