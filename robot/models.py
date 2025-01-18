from django.db import models
from django.contrib.auth import get_user_model


class TelegramUser(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='telegram_user'
    )
    chat_id = models.CharField(
        max_length=20
    )
    lang = models.CharField(
        max_length=10,
        null=True
    )

    def __str__(self) -> str:
        return self.chat_id

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
        self.save()


class BotText(models.Model):
    name = models.CharField(max_length=255, null=True)
    text = models.TextField()

    def __str__(self):
        return f'BotText {self.text[:20]}'


class BotImage(models.Model):
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='bot_images/')

    def __str__(self):
        return f'BotImage {self.name[:20]}'


class Offer(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    geo = models.CharField(max_length=255)
    traffic_type = models.CharField(max_length=255)
    offer_link = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Geos(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TrafficTypes(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CommunityButton(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name