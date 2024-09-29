import base64
import os
import tempfile
from datetime import timedelta
import uuid

from django.db.models import Count
from django.db.models.functions import TruncHour
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .address_verification import GMAPS, all_urzedy, get_closest_urzad
from .llm_prompts.qwen import ocr_pdf, submit_image, get_ocr_chat_messages
from .models import Conversation, Intent, Message
from .xml_generator import PCC3_6_Schema, generate_xml, validate_json_pcc3
from loguru import logger

import qrcode
from io import BytesIO

def chat_page(request):
    return render(request, "chat/chat.html")


class ChatAPIView(APIView):
    def get(self, request):
        return Response(
            {"message": "Welcome to the Chat API"}, status=status.HTTP_200_OK
        )

    def post(self, request):
        # Here you can handle chat messages
        message = request.data.get("message")
        # Process the message (you'll implement this later)
        return Response({"response": f"You said: {message}"}, status=status.HTTP_200_OK)


class FileUploadView(APIView):
    def post(self, request):
        logger.info(f"Received file upload request: {request.FILES}")
        file = request.FILES["file"]
        # Here you can process the file
        # save the file to the server
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            try:
                responses = ocr_pdf(temp_file.name)
            except Exception as e:
                responses = submit_image(temp_file.name, img_msg=get_ocr_chat_messages)

            return Response(
                {"message": "File uploaded successfully", "responses": responses}
            )

        return Response(
            {"message": "File uploaded successfully"}, status=status.HTTP_200_OK
        )


class XmlSchemaView(APIView):
    def get(self, request):
        return Response(
            {"message": PCC3_6_Schema.get_schema()}, status=status.HTTP_200_OK
        )


class ValidateUserDataView(APIView):
    def post(self, request):
        data = request.data
        try:
            validate_json_pcc3(data)
            return Response(
                {"message": "User data validated successfully", "data": data},
                status=status.HTTP_200_OK,
            )
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
                response = Response(f.read(), content_type="application/xml")
                response["Content-Disposition"] = (
                    'attachment; filename="deklaracja.xml"'
                )
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
                "all_urzedy": all_urzedy,
            }
        )


class AdminConversationsView(APIView):
    def get(self, request):
        try:
            # Get the current time and the time 24 hours ago
            now = timezone.now()
            day_ago = now - timedelta(days=1)

            # Query for conversations in the last 24 hours
            conversations = Conversation.objects.filter(created_at__gte=day_ago)

            # Query for intents in the last 24 hours, join with Message
            intents = Intent.objects.filter(
                message__conversation__in=conversations
            ).select_related("message__conversation")

            # Group by hour and intent, count messages
            stats = (
                intents.annotate(hour=TruncHour("message__conversation__created_at"))
                .values("hour", "intent")
                .annotate(count=Count("id"))
                .order_by("hour", "intent")
            )

            # Count messages per hour
            messages = (
                Message.objects.filter(conversation__in=conversations)
                .annotate(hour=TruncHour("conversation__created_at"))
                .values("hour")
                .annotate(count=Count("id"))
                .order_by("hour")
            )

            conversations_grouped_by_hour = (
                conversations.annotate(hour=TruncHour("created_at"))
                .values("hour")
                .annotate(count=Count("id"))
            )

            # Format the data for response
            formatted_stats = {}
            for stat in stats:
                hour_key = stat["hour"].isoformat()
                intent = stat["intent"]
                if hour_key not in formatted_stats:
                    formatted_stats[hour_key] = {}
                formatted_stats[hour_key][intent] = stat["count"]

            messages_stats = {}
            for stat in messages:
                hour_key = stat["hour"].isoformat()
                if hour_key not in messages_stats:
                    messages_stats[hour_key] = {}
                messages_stats[hour_key]["messages"] = stat["count"]

            conversations_stats = {}
            for stat in conversations_grouped_by_hour:
                hour_key = stat["hour"].isoformat()
                if hour_key not in conversations_stats:
                    conversations_stats[hour_key] = {}
                conversations_stats[hour_key]["conversations"] = stat["count"]

            return Response(
                {
                    "stats": formatted_stats,
                    "messages_stats": messages_stats,
                    "conversations_stats": conversations_stats,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InitializeConversationView(APIView):
    def get(self, request):
        multidevice_idx = uuid.uuid4()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://10.250.160.94:3000/mobileUpload/{multidevice_idx}")
        qr.make(fit=True)
        
        img = qr.make_image(fill="black", back_color="white").get_image()
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        base64_qr = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

        return Response(
            {
                "message": "Conversation initialized successfully",
                "multidevice_idx": multidevice_idx,
                "url": f"http://10.250.160.94:3000/mobileUpload/{multidevice_idx}",
                "qr": base64_qr,
            },
            status=status.HTTP_200_OK,
        )
