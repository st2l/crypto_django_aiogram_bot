from asgiref.sync import sync_to_async
from robot.models import Service

async def get_services_by_category(categories: list) -> list[Service]:
    all_services = await sync_to_async(
        Service.objects.all, thread_sensitive=True
    )()
    
    filtered_services = []
    async for service in all_services:
        if set(categories) & set(service.category.split()):
            filtered_services.append(service)
    
    return filtered_services 