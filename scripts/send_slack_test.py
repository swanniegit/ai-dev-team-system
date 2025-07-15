import os
from app.core.slack import send_slack_message

if __name__ == "__main__":
    channel = os.getenv("SLACK_TEST_CHANNEL") or input("Enter Slack channel (e.g. #general): ")
    text = os.getenv("SLACK_TEST_MESSAGE") or input("Enter message to send: ")
    success = send_slack_message(channel, text)
    if success:
        print("Message sent successfully!")
    else:
        print("Failed to send message.") 