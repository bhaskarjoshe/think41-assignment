from rest_framework import serializers

from .models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ["id", "user_id", "chat_id", "input_text", "llm_response", "timestamp"]
        read_only_fields = ["id", "timestamp"]
