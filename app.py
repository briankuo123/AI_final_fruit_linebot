# import flask related
from flask import Flask, request, abort
from urllib.parse import parse_qsl
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)
import json

# create flask server
app = Flask(__name__)
line_bot_api = LineBotApi('wf2GCBCfr20oOCC3zRI8nO//OQ+7O70dsX4oQyDd6OqKvVsPrpNUB7Nr9Am9CYFV0rY8wkFHNGLLn/E2Wjxmb96Kz64m1Gw9gHqpaxOWy75M8GkkWhhiNRWZQpOkbbFeXZiPwq1iNa7VStzalu8AeAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('65145590941570829a40b1fbfc5ff527')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name
    
    # get msg details
    print('msg from [', user_name, '](', user_id, ') : ', msg)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = msg))

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566)
