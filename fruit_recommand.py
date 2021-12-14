from urllib.parse import parse_qsl, parse_qs
import datetime
from linebot_import_api import *
import random

fruit_box=['草莓','奇異果','藍莓','西瓜','哈密瓜','木瓜','柳丁','檸檬','柚子','蘋果','楊桃','梨子','水蜜桃','李子','櫻桃','鳳梨','香蕉','蓮霧']
fruit_box_picture=['https://github.com/briankuo123/fruit_pic/blob/main/%E8%8D%89%E8%8E%93.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E5%A5%87%E7%95%B0%E6%9E%9C.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E8%97%8D%E8%8E%93.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E8%A5%BF%E7%93%9C.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E5%93%88%E5%AF%86%E7%93%9C.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%9C%A8%E7%93%9C.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%9F%B3%E4%B8%81.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%AA%B8%E6%AA%AC.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%9F%9A%E5%AD%90.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E8%98%8B%E6%9E%9C.png?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%A5%8A%E6%A1%83.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%B0%B4%E6%A2%A8.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%B0%B4%E8%9C%9C%E6%A1%83.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%9D%8E%E5%AD%90.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E6%AB%BB%E6%A1%83.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E9%B3%B3%E6%A2%A8.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E9%A6%99%E8%95%89.jpg?raw=true',
                    'https://github.com/briankuo123/fruit_pic/blob/main/%E8%93%AE%E9%9C%A7.jpg?raw=true']
fruit_season=[[0,5,6,7,10,14],
                [0,5,10],
                [0,5,10],
                [0,3,4,5,10,15],
                [0,2,3,4,5,10,13,14,15,16,17],
                [1,2,3,5,10,13,14,15,16,17],
                [1,2,3,5,7,9,10,12,13,14,16,17],
                [1,2,3,5,7,9,10,12,13,14,16],
                [1,2,5,7,9,10,11],
                [1,2,5,7,8,9,10,11],
                [1,4,5,6,7,8,9,10],
                [0,4,5,6,7,10,14]]
fruit_eye=[1,2,6,7,8,9,16]
fruit_beauty=[6,7,8,9,12]
fruit_digest=[1,2,9,15]
fruit_diet=[0,3,5,6,14,15]
fruit_rest=[1,7,9]

def fruit_recommand(event):
    message = TemplateSendMessage(
        alt_text='搜尋',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://img.ixintu.com/upload/jpg/20210523/d97c1b19cbb8967c78f6d3a759926c8e_46963_800_800.jpg!ys',
                    title='請問你注重下列哪一個項目呢?',
                    text='請在下方點選您注重的項目',
                    actions=[
                        PostbackAction(
                            label='當季水果',
                            display_text='我注重當季水果',
                            data='action=我注重當季水果'
                        ),
                        PostbackAction(
                            label='美白',
                            display_text='我注重幫助美白的水果',
                            data='action=我注重幫助美白的水果'
                        ),
                        PostbackAction(
                            label='顧眼睛',
                            display_text='我注重顧眼睛的水果',
                            data='action=我注重顧眼睛的水果'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://img.ixintu.com/upload/jpg/20210523/d97c1b19cbb8967c78f6d3a759926c8e_46963_800_800.jpg!ys',
                    title='請問你注重下列哪一個項目呢?',
                    text='請在下方點選您注重的項目',
                    actions=[
                        PostbackAction(
                            label='助消化',
                            display_text='我注重幫助消化的水果',
                            data='action=我注重幫助消化的水果'
                        ),
                        PostbackAction(
                            label='減肥',
                            display_text='我注重幫助減肥的水果',
                            data='action=我注重幫助減肥的水果'
                        ),
                        PostbackAction(
                            label='消除疲勞',
                            display_text='我注重幫助消除疲勞的水果',
                            data='action=我注重幫助消除疲勞的水果'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
def call_service(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://img.ixintu.com/upload/jpg/20210523/d97c1b19cbb8967c78f6d3a759926c8e_46963_800_800.jpg!ys',
            title='請問你注重下列哪一個項目呢?',
            text='請在下方點選您注重的項目',
            actions=[
                MessageAction(
                    label='當季水果',
                    text='我注重當季水果'
                ),
                MessageAction(
                    label='美白',
                    text='我注重幫助美白的水果'
                ),
                MessageAction(
                    label='顧眼睛',
                    text='我注重顧眼睛的水果'
                ),
                MessageAction(
                    label='助消化',
                    text='我注重幫助消化的水果'
                ),
                MessageAction(
                    label='減肥',
                    text='我注重幫助減肥的水果'
                ),
                MessageAction(
                    label='消除疲勞',
                    text='我注重幫助消除疲勞的水果的水果'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def sesonal_fruit():
    tonow = datetime.datetime.now()
    return random.choice(fruit_season[tonow.month-1])


