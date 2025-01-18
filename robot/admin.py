from django.contrib import admin

from .models import TelegramUser, BotImage, BotText, Offer, Geos, Categories, TrafficTypes


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user', 'id']


class BotTextAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'id']


class BotImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'id']


class OfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'geo',
                    'traffic_type', 'offer_link', 'id']


class GeosAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'id']


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'id']


class TrafficTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(BotImage, BotImageAdmin)
admin.site.register(BotText, BotTextAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Geos, GeosAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(TrafficTypes, TrafficTypesAdmin)
