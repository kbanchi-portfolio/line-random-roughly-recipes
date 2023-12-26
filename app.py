import os
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import TemplateSendMessage
from linebot.models import CarouselColumn
from linebot.models import CarouselTemplate
from linebot.models import URIAction

from cookpad import get_recipes

load_dotenv()

app = Flask(__name__)

line_api = LineBotApi(os.environ["ACCESS_TOKEN"])  # Initialize LINE API
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])  # Initialize WebhookHandler


@app.route("/")
def index():
    return "Hello Line Random Roughly Recipes"


@app.route("/push")
def push():
    user_id = os.environ["USER_ID"]
    line_api.push_message(user_id, TextSendMessage(text="Hello LINE"))  # Send message
    return "Push Send OK"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)  # Handle message
    except InvalidSignatureError:
        abort(400)
    return "Callback OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    Handler for message events
    """
    message = event.message.text
    recipes = get_recipes(message)  # Get recipes
    notes = [
        CarouselColumn(
            thumbnail_image_url=recipes[0]["image"],
            title=recipes[0]["name"],
            text=f"{message} recipe",
            actions=[URIAction(label="See recipe", uri=recipes[0]["link"])],
        ),
        CarouselColumn(
            thumbnail_image_url=recipes[1]["image"],
            title=recipes[1]["name"],
            text=f"{message} recipe",
            actions=[URIAction(label="See recipe", uri=recipes[1]["link"])],
        ),
        CarouselColumn(
            thumbnail_image_url=recipes[2]["image"],
            title=recipes[2]["name"],
            text=f"{message} recipe",
            actions=[URIAction(label="See recipe", uri=recipes[2]["link"])],
        ),
    ]
    reply = TemplateSendMessage(
        alt_text="template",
        template=CarouselTemplate(columns=notes),
    )
    line_api.reply_message(event.reply_token, messages=reply)  # Reply message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run application
