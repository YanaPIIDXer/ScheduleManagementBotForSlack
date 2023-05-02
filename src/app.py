import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import logging
import re
import json
from chatgpt import ChatBot, promptTemplate

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]

app = App(token=slack_bot_token, process_before_response=True)

# ChatGPTに投げる
def think(channel, message, thread_ts, say):
    bot = ChatBot(os.environ["OPENAI_API_KEY"])
    bot.set_simple_template(promptTemplate, ["input"])
    result = bot.run({ "input": message })
    say(result, thread_ts=thread_ts)

# メンション受信イベント
@app.event("app_mention")
def handle_mention(event, say, logger):
    message = re.sub(r'^<.*>', '', event['text'])   # メンション除去
    channel = event["channel"]
    thread_ts = event.get("thread_ts", None) or event["ts"]     # スレッド

    think(channel, message, thread_ts, say)

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def handler(event, context):
    # HACK: リトライは弾く
    if event["header"]["X-Slack-Retry-Num"] != None:
        return {
            "statusCode": 200,
            "body": json.dumps("OK"),
        }
    slack_handler = SlackRequestHandler(app)
    return slack_handler.handle(event, context)
