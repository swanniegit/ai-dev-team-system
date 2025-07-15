import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_message(channel, text, token=None):
    """Send a message to a Slack channel."""
    slack_token = token or os.getenv("SLACK_BOT_TOKEN")
    if not slack_token:
        logging.error("Slack token not provided or set in environment.")
        return False
    client = WebClient(token=slack_token)
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        logging.info(f"Slack message sent: {response['ts']}")
        return True
    except SlackApiError as e:
        logging.error(f"Slack API error: {e.response['error']}")
        return False 