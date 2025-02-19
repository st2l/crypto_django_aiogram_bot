import logging
from robot.models import Offer
from asgiref.sync import sync_to_async


async def get_offers_by_data(data: dict) -> list[Offer]:
    all_offers = await sync_to_async(
        Offer.objects.all, thread_sensitive=True
    )()

    ans = []
    logging.info(f'Data: {data}')
    
    async for offer in all_offers:
        
        logging.info(set(offer.category.split()), set(offer.geo.split()), set(offer.traffic_type.split()))
        logging.info(set(data['category']) & set(offer.category.split()))
        logging.info(set(data['geo']) & set(offer.geo.split()))
        logging.info(set(data['traffic_type']) & set(offer.traffic_type.split()))
        
        if (set(data['category']) & set(offer.category.split())) and \
            (set(data['geo']) & set(offer.geo.split())) and \
                (set(data['traffic_type']) & set(offer.traffic_type.split())):
            ans.append(offer)
    
    return ans
