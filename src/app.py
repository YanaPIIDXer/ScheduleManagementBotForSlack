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
def think(channel, message, thread_ts, sender, say):
    bot = ChatBot(os.environ["OPENAI_API_KEY"])
    bot.set_simple_template(promptTemplate, ["input"])
    summarizedJsonText = bot.run({ "input": message })
    summarizedData = json.loads(summarizedJsonText)
    if summarizedData["is_valid"] == False:
        msg = f"<@{sender}>スケジュールを抽出できませんでした"
        return say(msg, thread_ts)
    
    start_dt = summarizedData["start_date_time"]
    end_dt = summarizedData["end_date_time"]
    title = summarizedData["title"]
    summary = summarizedData["summary"]
    # TODO: 実際にGoogleカレンダーに登録する処理の実装
    msg = f"""
    <@{sender}>
    以下の内容でカレンダーに登録しました。
    
    タイトル:
    {title}
    説明:
    {summary}
    開始日時:
    {start_dt}
    終了日時:
    {end_dt}
    """
    say(msg, thread_ts=thread_ts)

# メンション受信イベント
@app.event("app_mention")
def handle_mention(event, say):
    message = re.sub(r'^<.*>', '', event['text'])   # メンション除去
    channel = event["channel"]
    thread_ts = event.get("thread_ts", None) or event["ts"]     # スレッド

    think(channel, message, thread_ts, event["user"], say)

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def handler(event, context):
    # HACK: リトライは弾く
    if "X-Slack-Retry-Num" in event["headers"] and int(event["headers"]["X-Slack-Retry-Num"]) > 1:
        print("Retry:" + event["headers"]["X-Slack-Retry-Num"])
        return {
            "statusCode": 200,
            "body": json.dumps("OK"),
        }
    slack_handler = SlackRequestHandler(app)
    return slack_handler.handle(event, context)
