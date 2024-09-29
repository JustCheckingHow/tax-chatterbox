import uuid

from django.db import models


class Conversation(models.Model):
    conversation_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=True)

    class Meta:
        ordering = ["timestamp"]


class Intent(models.Model):
    message = models.ForeignKey(
        Message, related_name="intents", on_delete=models.CASCADE
    )
    intent = models.CharField(max_length=255)


class Cost(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="costs", on_delete=models.CASCADE
    )
    cost = models.FloatField()
