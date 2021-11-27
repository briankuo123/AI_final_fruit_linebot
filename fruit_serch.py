from urllib.parse import parse_qsl, parse_qs
import datetime
from linebot_import_api import *

def fruit_serch(event):
    message = TemplateSendMessage(
        alt_text='索取備品',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='漿果類',
                    text='請選擇要查詢的水果',
                    actions=[
                        PostbackAction(
                            label='草莓',
                            display_text='查詢草莓',
                            data='action=查詢草莓&item=草莓'
                        ),
                        PostbackAction(
                            label='奇異果',
                            display_text='查詢奇異果',
                            data='action=查詢奇異果&item=奇異果'
                        ),
                        PostbackAction(
                            label='藍莓',
                            display_text='查詢藍莓',
                            data='action=查詢藍莓&item=藍莓'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='瓜果類',
                    text='請選擇要查詢的水果',
                    actions=[
                        PostbackAction(
                            label='西瓜',
                            display_text='查詢西瓜',
                            data='action=查詢西瓜&item=西瓜'
                        ),
                        PostbackAction(
                            label='哈密瓜',
                            display_text='查詢哈密瓜',
                            data='action=查詢哈密瓜&item=哈密瓜'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
