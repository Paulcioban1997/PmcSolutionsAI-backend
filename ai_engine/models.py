from django.conf import settings
from django.db import models


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Conversation")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20)  # user/assistant
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Usage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
