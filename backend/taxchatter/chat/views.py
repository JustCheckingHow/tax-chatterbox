import os
import tempfile

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import HttpResponse, Response
from rest_framework.views import APIView
from xml_generator import generate_xml, required_fields, validate_user_data

from .address_verification import GMAPS, get_closest_urzad
from .llm_prompts.qwen import ocr_pdf


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
            responses = ocr_pdf(temp_file.name)

            return Response({"message": "File uploaded successfully", "responses": responses})

        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)


class XmlSchemaView(APIView):
    def get(self, request):
        return Response({"message": required_fields}, status=status.HTTP_200_OK)


class ValidateUserDataView(APIView):
    def post(self, request):
        data = request.data
        try:
            validate_user_data(data)
            return Response({"message": "User data validated successfully", "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerateXmlView(APIView):
    # allow user to download generated file

    def post(self, request):
        data = request.data
        try:
            # Generate XML using the data
            temp_file_name = generate_xml(data)

            with open(temp_file_name) as f:
                response = HttpResponse(f.read(), content_type="application/xml")
                response["Content-Disposition"] = 'attachment; filename="deklaracja.xml"'
                os.remove(temp_file_name)
                return response

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LocationView(APIView):
    def post(self, request):
        user_location = request.data.get("location")
        # Here you can process the location

        top3_closest = get_closest_urzad(GMAPS, user_location)
        return Response(
            {
                "message": "Location processed successfully",
                "closest": top3_closest,
                "user_location": user_location,
            }
        )
