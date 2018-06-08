from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    chat_name = models.CharField(max_length=30, unique=True)
    chat_link = models.CharField(max_length=30, unique=True)
    is_private = models.BooleanField(default=False)
    pass_hash = models.CharField(max_length=32)
    image = models.ImageField(default="chat_avatar/1.jpg", upload_to="chat_avatar")

    def __str__(self):
        return self.chat_name


class AvailableUser(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Message(models.Model):
    message_context = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date"]
