from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def chat_page(request):
    return render(request, 'chat/chat.html')

class ChatAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Chat API"}, status=status.HTTP_200_OK)

    def post(self, request):
        # Here you can handle chat messages
        message = request.data.get('message')
        # Process the message (you'll implement this later)
        return Response({"response": f"You said: {message}"}, status=status.HTTP_200_OK)