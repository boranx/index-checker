import unittest
import sys
import slackweb

from mock import patch, MagicMock

sys.path.append("../")
sys.path.append("../src")
from src.slack import Slack


class ElasticSearchServiceTests(unittest.TestCase):
    def test_should_invoke_notify(self):
        msg = "notifier"
        with patch('src.slack.Slack') as mock:
                    instance = mock.return_value
                    instance.notify.return_value = msg
        result = instance.notify(msg)
        self.assertIsNotNone(result)

    def test_should_invoke_notify_method(self):
        msg = "notifier"
        slack_uri = "http://dummy"
        with patch('slackweb.Slack.notify') as notified:
            slack = Slack(slack_uri)
            slack.notify(msg)
            notified.assert_called_once_with(text=msg)
