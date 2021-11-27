from urllib.parse import parse_qsl, parse_qs
import datetime
from linebot_import_api import *

def fruit_serch(event):
    message = TemplateSendMessage(
        alt_text='搜尋',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='漿果類',
                    text='請選擇想查詢的水果',
                    actions=[
                        PostbackAction(
                            label='草莓',
                            display_text='查詢草莓',
                            data='action=查詢草莓'
                        ),
                        PostbackAction(
                            label='奇異果',
                            display_text='查詢奇異果',
                            data='action=查詢奇異果'
                        ),
                        PostbackAction(
                            label='藍莓',
                            display_text='查詢藍莓',
                            data='action=查詢藍莓'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='瓜果類',
                    text='請選擇想查詢的水果',
                    actions=[
                        PostbackAction(
                            label='西瓜',
                            display_text='查詢西瓜',
                            data='action=查詢西瓜'
                        ),
                        PostbackAction(
                            label='哈密瓜',
                            display_text='查詢哈密瓜',
                            data='action=查詢哈密瓜'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='柑橘類',
                    text='請選擇想查詢的水果',
                    actions=[
                        PostbackAction(
                            label='柳丁',
                            display_text='查詢柳丁',
                            data='action=查詢柳丁'
                        ),
                        PostbackAction(
                            label='檸檬',
                            display_text='查詢檸檬',
                            data='action=查詢檸檬'
                        ),
                        PostbackAction(
                            label='柚子',
                            display_text='查詢柚子',
                            data='action=查詢柚子'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
