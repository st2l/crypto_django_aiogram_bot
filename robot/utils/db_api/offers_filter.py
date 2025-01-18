from robot.models import Offer
from asgiref.sync import sync_to_async


async def get_offers_by_data(data: dict):
    all_offers = await sync_to_async(
        Offer.objects.all, thread_sensitive=True
    )()

    ans = []
    async for offer in all_offers:
        if (data['category'] in offer.category) and \
            (data['geo'] in offer.geo) and \
                (data['traffic_type'] in offer.traffic_type):
            ans.append(offer)
    
    return ans
