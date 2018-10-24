import slackweb


class Slack:
    def __init__(self, slack_URL):
        self.slack = slackweb.Slack(url=slack_URL)

    def notify(self, message):
        self.slack.notify(text=message)
