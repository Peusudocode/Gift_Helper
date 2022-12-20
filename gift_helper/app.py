# -*- coding: UTF-8 -*-
import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pygraphviz
from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
load_dotenv()


machine = TocMachine(
    states=[
        "user",
        "introduction",
        "start_query",
        "input_age",
        "input_gender",
        "input_festival",
        "input_money",
        "give_advise",
        "random_pick",
        "search_merchandise",
        "show_merchandise"
    ],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "introduction",
            "conditions": "is_going_to_introduction",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start_query",
            "conditions": "is_going_to_start_query",
        },
        {
            "trigger": "advance",
            "source": "start_query",
            "dest": "input_age",
            "conditions": "is_going_to_input_age",
        },
        {
            "trigger": "advance",
            "source": "input_age",
            "dest": "input_gender",
            "conditions": "is_going_to_input_gender",
        },
        {
            "trigger": "advance",
            "source": "input_gender",
            "dest": "input_festival",
            "conditions": "is_going_to_input_festival",
        },
        {
            "trigger": "advance",
            "source": "input_festival",
            "dest": "input_money",
            "conditions": "is_going_to_input_money",
        },
        {
            "trigger": "advance",
            "source": "input_money",
            "dest": "give_advise",
            "conditions": "is_going_to_give_advise",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "random_pick",
            "conditions": "is_going_to_random_pick",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search_merchandise",
            "conditions": "is_going_to_search_merchandise",
        },
        {
            "trigger": "advance",
            "source": "search_merchandise",
            "dest": "show_merchandise",
            "conditions": "is_going_to_show_merchandise",
        },
        {"trigger": "go_back",
         "source": [
            "introduction",
            "start_query",
            "input_age",
            "input_gender",
            "input_festival",
            "input_money",
            "give_advise",
            "random_pick",
            "search_merchandise",
            "show_merchandise"
         ],
         "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = machine.advance(event)

        if response == False:
            text = '歡迎使用禮物挑選小幫手。\n輸入『開始挑選』就會問你問題，給你禮物建議。' \
               '\n輸入『重新開始』就能重新開始\n輸入『查詢』就可以自動幫你搜尋商品名稱與價格。\n輸入『隨機挑選』就可以隨機給你禮物建議。'
            send_text_message(event.reply_token, text)
            machine.go_back(event)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    # machine.get_graph().draw("fsm.png", prog="dot", format="png")
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
