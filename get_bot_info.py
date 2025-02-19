from robot.models import BotText, BotImage
import logging
from asgiref.sync import sync_to_async

async def get_bot_text(param: str) -> str:
    try:
        
        bot_text = await BotText.objects.aget(name__contains=param)
        logging.info(bot_text)
        
        return bot_text.text
        
    except Exception as e:
        bot_text = await BotText.objects.acreate(name=param, text='тестовый текст')
        return bot_text.text

async def get_bot_image(param: str) -> str:
    try:
        
        bot_image = await BotImage.objects.aget(name__contains=param)
        logging.info(bot_image)
        
        return bot_image.image.path
        
    except Exception as e:
        logging.exception(e)
