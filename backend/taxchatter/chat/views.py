import tempfile

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .llm_prompts.qwen import extract_pdf


def chat_page(request):
    return render(request, "chat/chat.html")


class ChatAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Chat API"}, status=status.HTTP_200_OK)

    def post(self, request):
        # Here you can handle chat messages
        message = request.data.get("message")
        # Process the message (you'll implement this later)
        return Response({"response": f"You said: {message}"}, status=status.HTTP_200_OK)


class FileUploadView(APIView):
    def post(self, request):
        file = request.FILES["file"]
        # Here you can process the file
        # save the file to the server
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            responses = extract_pdf(temp_file.name)

            return Response({"message": "File uploaded successfully", "responses": responses})

        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
