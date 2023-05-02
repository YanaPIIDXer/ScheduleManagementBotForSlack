import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import openai
import logging
import re

openai.api_key = os.environ["OPENAI_API_KEY"]
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]

app = App(token=slack_bot_token, process_before_response=True)

@app.event("app_mention")
def handle_mention(event, say, logger):
    logger.info(event)
    message = re.sub(r'^<.*>', '', event['text'])   # メンション除去
    # とりあえずオウム返し
    say(f"<@{event['user']}>{message}")

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def handler(event, context):
    slack_handler = SlackRequestHandler(app)
    return slack_handler.handle(event, context)
