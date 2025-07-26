from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .llm import build_prompt, get_llm_response
from .models import ChatHistory
from .serialzers import ChatHistorySerializer


class ChatView(APIView):
    def get(self, request):
        return Response({"message": "POST your chat input here."})

    def post(self, request, format=None):
        user_id = request.data.get("user_id")
        chat_id = request.data.get("chat_id")
        input_text = request.data.get("input_text")
        print(user_id, chat_id, input_text)
        if not all([chat_id, input_text, user_id]):
            return Response(
                {"error": "chat_id, input_text, and user_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        previous_contexts = ChatHistory.objects.filter(chat_id=chat_id).order_by(
            "-timestamp"
        )[:5]

        context_text = "\n".join(
            reversed([entry.llm_response for entry in previous_contexts])
        )

        prompt = build_prompt(context_text, input_text)
        llm_response = get_llm_response(input_text, prompt)
        print(llm_response)
        chat = ChatHistory.objects.create(
            user_id=user_id,
            chat_id=chat_id,
            input_text=input_text,
            llm_response=llm_response,
        )

        serializer = ChatHistorySerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
