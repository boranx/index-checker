import argparse


class Arguments:
    @staticmethod
    def get_params():
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', dest='SLACK_URL',
                            help='Slack Notifier Hook URI')
        return parser.parse_args()
        
    def return_slack_uri(self, parsed):
        if parsed.SLACK_URL:
            return parsed.SLACK_URL
        else:
            return ""
