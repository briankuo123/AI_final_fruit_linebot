from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, 
    PostbackEvent,
    TextMessage, 
    TextSendMessage, 
    ImageSendMessage, 
    StickerSendMessage, 
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    DatetimePickerAction,
    ConfirmTemplate
)

line_bot_api = LineBotApi('wf2GCBCfr20oOCC3zRI8nO//OQ+7O70dsX4oQyDd6OqKvVsPrpNUB7Nr9Am9CYFV0rY8wkFHNGLLn/E2Wjxmb96Kz64m1Gw9gHqpaxOWy75M8GkkWhhiNRWZQpOkbbFeXZiPwq1iNa7VStzalu8AeAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('65145590941570829a40b1fbfc5ff527')
