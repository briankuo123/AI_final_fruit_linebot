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
                    title='毛巾類',
                    text='請問想索取哪一種備品',
                    actions=[
                        PostbackAction(
                            label='毛巾',
                            display_text='想索取毛巾',
                            data='action=索取備品&item=毛巾'
                        ),
                        PostbackAction(
                            label='浴巾',
                            display_text='想索取浴巾',
                            data='action=索取備品&item=浴巾'
                        ),
                        PostbackAction(
                            label='方巾',
                            display_text='想索取方巾',
                            data='action=索取備品&item=方巾'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='清潔用品',
                    text='請問想索取哪一種請潔用品',
                    actions=[
                        PostbackAction(
                            label='沐浴乳',
                            display_text='想索取沐浴乳',
                            data='action=索取備品&item=沐浴乳'
                        ),
                        PostbackAction(
                            label='洗髮精',
                            display_text='想索取洗髮精',
                            data='action=索取備品&item=洗髮精'
                        ),
                        PostbackAction(
                            label='乳液',
                            display_text='想索取乳液',
                            data='action=索取備品&item=乳液'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='其他備品',
                    text='請問想索取哪一種備品',
                    actions=[
                        PostbackAction(
                            label='礦泉水',
                            display_text='想索取礦泉水',
                            data='action=索取備品&item=礦泉水'
                        ),
                        PostbackAction(
                            label='3合1沖泡咖啡包',
                            display_text='想索取3合1沖泡咖啡包',
                            data='action=索取備品&item=3合1沖泡咖啡包'
                        ),
                        PostbackAction(
                            label='紅茶茶包',
                            display_text='想索取紅茶茶包',
                            data='action=索取備品&item=紅茶茶包'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
