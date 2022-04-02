from flask import Flask, request, abort, url_for, render_template
from urllib.parse import parse_qsl, parse_qs
import random
from linebot.models import events
from linebot_import_api import *
from fruit_serch import *
from fruit_recommand import*
from keras.models import load_model
from crawler import*
from PIL import Image, ImageOps
import numpy as np
import pyimgur

client_id = '93f159998fb38d7'
client_secret = '933c603016c7848acc80955c7bab15d34a2ab26a'
result=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
link=["https://aifruitnew.azurewebsites.net/static/price_chart_0.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_1.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_2.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_3.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_4.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_5.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_6.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_7.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_8.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_9.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_10.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_11.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_12.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_13.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_14.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_15.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_16.png",
        "https://aifruitnew.azurewebsites.net/static/price_chart_17.png",]

def upload_chart():
    PATH = "price_chart.png"
    im = pyimgur.Imgur('93f159998fb38d7')
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link

def get_result(id):
    return 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descript')
def descript():
    return render_template('descript.html')

@app.route('/function')
def function():
    return render_template('function.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route("/maintain")
def maintain():
    global result
    for i in range (18):
        result[i]=craw_fruit(i)
        if result[i][0] != -1:
            plt.plot(result[i][3],result[i][2],"r")
            plt.title("whole year price")
            plt.xlabel('date')
            plt.ylabel('price')
            plt.xticks(rotation=45)
            x_locator=MultipleLocator(50)
            y_locator=MultipleLocator(20)
            ax=plt.gca()
            ax.xaxis.set_major_locator(x_locator)
            ax.yaxis.set_major_locator(y_locator)
            plt.savefig('./static/price_chart_'+str(i)+'.png', bbox_inches='tight')
            plt.close()
    return 'ok'

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
        if result[0][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[0][1])+' ' +str(result[0][0])+'元\n'+str(result[0][4])))
            messages.append(ImageSendMessage(original_content_url=link[0],
                                                preview_image_url=link[0]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢奇異果':
        messages=[]
        messages.append(TextSendMessage(text='奇異果 每100克\n熱量:61千卡\n糖:9.0克\n維生素C:92.7毫克\n膳食纖維3.0毫克\n鉀質:312毫克'))       
        if result[1][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[1][1])+' ' +str(result[1][0])+'元\n'+str(result[1][4])))
            messages.append(ImageSendMessage(original_content_url=link[1],
                                                preview_image_url=link[1]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢藍莓':
        messages=[]
        messages.append(TextSendMessage(text='藍莓 每100克\n熱量:57千卡\n糖:10.0克\n維生素C:9.7毫克\n膳食纖維2.4毫克'))   
        if result[2][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[2][1])+' ' +str(result[2][0])+'元\n'+str(result[2][4])))
            messages.append(ImageSendMessage(original_content_url=link[2],
                                                preview_image_url=link[2]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢西瓜':
        messages=[]
        messages.append(TextSendMessage(text='西瓜 每100克\n熱量:30千卡\n糖:6.2克\n維生素C:8.1毫克\n膳食纖維0.4毫克\nβ-胡蘿蔔素:303微克'))  
        if result[3][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[3][1])+' ' +str(result[3][0])+'元\n'+str(result[3][4])))
            messages.append(ImageSendMessage(original_content_url=link[3],
                                                preview_image_url=link[3]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢哈密瓜':
        messages=[]
        messages.append(TextSendMessage(text='哈密瓜 每100克\n熱量:34千卡\n糖:7.9克\n維生素C:36.7毫克\n膳食纖維0.9毫克\n鉀質:267微克\nβ-胡蘿蔔素:2020微克'))      
        if result[4][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[4][1])+' ' +str(result[4][0])+'元\n'+str(result[4][4])))
            messages.append(ImageSendMessage(original_content_url=link[4],
                                                preview_image_url=link[4]))  
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢木瓜':
        messages=[]
        messages.append(TextSendMessage(text='木瓜 每100克\n熱量:38千卡\n糖:6.2克\n維生素C:58.3毫克\n膳食纖維1.4毫克\n鉀質:186微克\nβ-胡蘿蔔素:399微克')) 
        if result[5][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[5][1])+' ' +str(result[5][0])+'元\n'+str(result[5][4])))
            messages.append(ImageSendMessage(original_content_url=link[5],
                                                preview_image_url=link[5]))
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)      
    elif postback_data.get('action')=='查詢柳丁':
        messages=[]
        messages.append(TextSendMessage(text='柳丁 每100克\n熱量:47千卡\n糖:9.4克\n維生素C:53.2毫克\n膳食纖維2.4毫克'))      
        if result[6][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[6][1])+' ' +str(result[6][0])+'元\n'+str(result[6][4])))
            messages.append(ImageSendMessage(original_content_url=link[6],
                                                preview_image_url=link[6]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢檸檬':
        messages=[]
        messages.append(TextSendMessage(text='柳丁 每100克\n熱量:29千卡\n糖:2.5克\n維生素C:53.0毫克\n膳食纖維2.8毫克\n鐵質:0.6毫克'))
        if result[7][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[7][1])+' ' +str(result[7][0])+'元\n'+str(result[7][4])))
            messages.append(ImageSendMessage(original_content_url=link[7],
                                                preview_image_url=link[7]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢柚子':
        messages=[]
        messages.append(TextSendMessage(text='柚子 每100克\n熱量:40千卡\n糖:7.2克\n維生素C:59.0毫克\n膳食纖維1.3毫克\n鉀質:200毫克'))      
        if result[8][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[8][1])+' ' +str(result[8][0])+'元\n'+str(result[8][4])))
            messages.append(ImageSendMessage(original_content_url=link[8],
                                                preview_image_url=link[8]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢蘋果':
        messages=[]
        messages.append(TextSendMessage(text='蘋果 每100克\n熱量:52千卡\n糖:10.4克\n維生素C:4.6毫克\n膳食纖維:2.4毫克')) 
        if result[9][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[9][1])+' ' +str(result[9][0])+'元\n'+str(result[9][4])))
            messages.append(ImageSendMessage(original_content_url=link[9],
                                                preview_image_url=link[9]))  
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢楊桃':
        messages=[]
        messages.append(TextSendMessage(text='楊桃 每100克\n熱量:31千卡\n糖:4.0克\n維生素C:34.4毫克\n膳食纖維2.8毫克'))
        if result[10][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[10][1])+' ' +str(result[10][0])+'元\n'+str(result[10][4])))
            messages.append(ImageSendMessage(original_content_url=link[10],
                                                preview_image_url=link[10]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢梨子':
        messages=[]
        messages.append(TextSendMessage(text='梨子 每100克\n熱量:42千卡\n糖:7.1克\n維生素C:3.8毫克\n膳食纖維3.6毫克\n鉀質:121毫克'))      
        if result[11][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[11][1])+' ' +str(result[11][0])+'元\n'+str(result[11][4])))
            messages.append(ImageSendMessage(original_content_url=link[11],
                                                preview_image_url=link[11]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢水蜜桃':
        messages=[]
        messages.append(TextSendMessage(text='水蜜桃 每100克\n熱量:39千卡\n糖:8.4克\n維生素C:6.6毫克\n膳食纖維1.5毫克'))  
        if result[12][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[12][1])+' ' +str(result[12][0])+'元\n'+str(result[12][4])))
            messages.append(ImageSendMessage(original_content_url=link[12],
                                                preview_image_url=link[12]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢李子':
        messages=[]
        messages.append(TextSendMessage(text='李子 每100克\n熱量:46千卡\n糖:9.9克\n維生素C:9.5毫克\n膳食纖維1.4毫克'))        
        if result[13][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[13][1])+' ' +str(result[13][0])+'元\n'+str(result[13][4])))
            messages.append(ImageSendMessage(original_content_url=link[13],
                                                preview_image_url=link[13]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢櫻桃':
        messages=[]
        messages.append(TextSendMessage(text='櫻桃 每100克\n熱量:63千卡\n糖:12.8克\n維生素C:7.0毫克\n膳食纖維2.1毫克\n鉀質:222毫克'))  
        if result[14][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[14][1])+' ' +str(result[14][0])+'元\n'+str(result[14][4])))
            messages.append(ImageSendMessage(original_content_url=link[14],
                                                preview_image_url=link[14]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢鳳梨':
        messages=[]
        messages.append(TextSendMessage(text='鳳梨 每100克\n熱量:50千卡\n糖:9.9克\n維生素C:47.8毫克\n膳食纖維1.4毫克'))        
        if result[15][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[15][1])+' ' +str(result[15][0])+'元\n'+str(result[15][4])))
            messages.append(ImageSendMessage(original_content_url=link[15],
                                                preview_image_url=link[15]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢香蕉':
        messages=[]
        messages.append(TextSendMessage(text='香蕉 每100克\n熱量:89千卡\n糖:12.2克\n維生素C:8.7毫克\n膳食纖維2.6毫克\n鉀質:358毫克'))      
        if result[16][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[16][1])+' ' +str(result[16][0])+'元\n'+str(result[16][4])))
            messages.append(ImageSendMessage(original_content_url=link[16],
                                                preview_image_url=link[16]))    
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='查詢蓮霧':
        messages=[]
        messages.append(TextSendMessage(text='蓮霧 每100克\n熱量:35千卡\n糖:6.7克\n維生素C:11.0毫克\n膳食纖維1.0毫克'))       
        if result[17][0] != -1:
            messages.append(TextSendMessage(text='最近價格為'+ str(result[17][1])+' ' +str(result[17][0])+'元\n'+str(result[17][4])))
            messages.append(ImageSendMessage(original_content_url=link[17],
                                                preview_image_url=link[17]))   
        else: 
            messages.append(TextSendMessage(text='無法獲取市場價格'))
        line_bot_api.reply_message(event.reply_token, messages) 
    elif postback_data.get('action')=='我注重當季水果':
        recommand=sesonal_fruit()
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[recommand])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[recommand],
                                                preview_image_url=fruit_box_picture[recommand]))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='我注重幫助美白的水果':
        ran=random.choice(fruit_beauty)
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[ran])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[ran],
                                                preview_image_url=fruit_box_picture[ran]))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='我注重顧眼睛的水果':
        ran=random.choice(fruit_eye)
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[ran])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[ran],
                                                preview_image_url=fruit_box_picture[ran]))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='我注重幫助消化的水果':
        ran=random.choice(fruit_digest)
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[ran])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[ran],
                                                preview_image_url=fruit_box_picture[ran]))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='我注重幫助減肥的水果':
        ran=random.choice(fruit_diet)
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[ran])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[ran],
                                                preview_image_url=fruit_box_picture[ran]))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='我注重幫助消除疲勞的水果':
        ran=random.choice(fruit_rest)
        messages=[]
        messages.append(TextSendMessage(text='為你推薦{}'.format(fruit_box[ran])))
        messages.append(ImageSendMessage(original_content_url=fruit_box_picture[ran],
                                                preview_image_url=fruit_box_picture[ran]))
        line_bot_api.reply_message(event.reply_token, messages)              

@handler.add(MessageEvent)
def handle_something(event):
    if event.message.type=='text':
        recrive_text=event.message.text
        if '水果資訊查詢' in recrive_text:
            fruit_serch(event)
        elif '今日推薦水果' in recrive_text:
            fruit_recommand(event)
        elif '水果熟度辨識' in recrive_text:
            messages=[]
            messages.append(TextSendMessage(text='在此聊天室傳香蕉的照片就可以開始辨識熟度了喔!'))
            line_bot_api.reply_message(event.reply_token, messages)    
        else:
            messages=[]
            messages.append(TextSendMessage(text='很抱歉我們無法了解你所輸入的內容，請再輸入一次'))
            line_bot_api.reply_message(event.reply_token, messages)  
    elif event.message.type=='image':
        model = load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        message_content = line_bot_api.get_message_content(event.message.id)
        with open('temp.jpg', 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        image = Image.open('temp.jpg')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        messages=[]
        if prediction.argmax()==0 :
            messages.append(TextSendMessage(text='您的香蕉熟度正好'))
            line_bot_api.reply_message(event.reply_token, messages) 
        elif prediction.argmax()==1 :
            messages.append(TextSendMessage(text='您的香蕉熟度過熟'))
            line_bot_api.reply_message(event.reply_token, messages)
        elif prediction.argmax()==2 :
            messages.append(TextSendMessage(text='您的香蕉熟度不足'))
            line_bot_api.reply_message(event.reply_token, messages)
        elif prediction.argmax()==3 :
            messages.append(TextSendMessage(text='我們無法偵測到畫面有香蕉'))
            line_bot_api.reply_message(event.reply_token, messages)      
    else:
        messages=[]
        messages.append(TextSendMessage(text='很抱歉我們只能接收文字訊息，請改輸入文字'))
        line_bot_api.reply_message(event.reply_token, messages)

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5003, debug=True)

