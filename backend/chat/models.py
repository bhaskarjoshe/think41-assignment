import uuid

from django.db import models


class ChatHistory(models.Model):
    user_id = models.CharField(max_length=100, db_index=True)
    chat_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    input_text = models.TextField()
    llm_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_history"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"User {self.user_id} | Chat {self.chat_id} at {self.timestamp}"
