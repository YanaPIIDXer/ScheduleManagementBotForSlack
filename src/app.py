import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import openai
import json

# openai.api_key = os.environ["OPENAI_API_KEY"]
# slack_bot_token = os.environ["SLACK_BOT_TOKEN"]

# slack = App(token=slack_bot_token)

# @slack.event("app_mention")
# def handle_mention(body, say):
#   pass

# handler = handle_mention

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps("Hello"),
    }

handler = handler
