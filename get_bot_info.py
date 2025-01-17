from robot.models import BotText
import logging
from asgiref.sync import sync_to_async

async def get_bot_text(param: str) -> str:
    try:
        
        bot_text = await BotText.objects.aget(name__contains=param)
        logging.info(bot_text)
        
        return bot_text.text
        
    except Exception as e:
        logging.exception(e)