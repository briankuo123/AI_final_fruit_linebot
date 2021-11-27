from flask import Flask, request, abort, url_for
from urllib.parse import parse_qsl, parse_qs
import random
from linebot.models import events
from linebot_import_api import *
from fruit_serch import *

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

#handle msg
import os
import speech_recognition as sr

def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    postback_data = dict(parse_qsl(event.postback.data))
    if postback_data.get('action')=='查詢草莓':
        messages=[]
        messages.append(TextSendMessage(text='草莓  每100克\n熱量:32千卡\n糖:4.9克\n維生素C:58.8毫克\n膳食纖維:2.0克'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢奇異果':
        messages=[]
        messages.append(TextSendMessage(text='奇異果 每100克\n熱量:61千卡\n糖:9.0克\n維生素C:92.7毫克\n膳食纖維3.0毫克\n鉀質:312毫克'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢藍莓':
        messages=[]
        messages.append(TextSendMessage(text='藍莓 每100克\n熱量:57千卡\n糖:10.0克\n維生素C:9.7毫克\n膳食纖維2.4毫克\n'))
        line_bot_api.reply_message(event.reply_token, messages)

@handler.add(MessageEvent)
def handle_something(event):
    if event.message.type=='text':
        recrive_text=event.message.text
        if '水果資訊查詢' in recrive_text:
            messages=[]
            messages.append(TextSendMessage(text='正在為你導入查詢頁面'))
            line_bot_api.reply_message(event.reply_token, messages)
            fruit_serch(event)
        elif '今日推薦水果' in recrive_text:
            fruit_box=['草莓','奇異果','藍莓']
            messages=[]
            messages.append(TextSendMessage(text='為你推薦 {}'.format(fruit_box[random.randint(0,2)])))
            line_bot_api.reply_message(event.reply_token, messages)
        elif '水果熟度辨識' in recrive_text:
            messages=[]
            messages.append(TextSendMessage(text='很抱歉我們還未將此功能導入，請改日再試'))
            line_bot_api.reply_message(event.reply_token, messages)
        else:
            messages=[]
            messages.append(TextSendMessage(text='很抱歉我們無法了解你所輸入的內容，請再輸入一次'))
            line_bot_api.reply_message(event.reply_token, messages)
    else:
        messages=[]
        messages.append(TextSendMessage(text='很抱歉我們只能接收文字訊息，請改輸入文字'))
        line_bot_api.reply_message(event.reply_token, messages)

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566, debug=True)