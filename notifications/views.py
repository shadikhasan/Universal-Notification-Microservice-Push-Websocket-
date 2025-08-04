# notifications/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notification
from django.contrib.auth import get_user_model
from .serializers import NotificationSendSerializer
from .authentication import APIKeyAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

# notifications/views.py (broadcast version)
class SendNotificationView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        tenant = request.user
        serializer = NotificationSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notif = Notification.objects.create(
            tenant=tenant,
            title=serializer.validated_data["title"],
            message=serializer.validated_data["message"],
            data=serializer.validated_data.get("data", {})
        )

        # Push to Redis/WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"tenant_{tenant.id}",
            {
                "type": "notify",
                "data": {
                    "title": notif.title,
                    "message": notif.message,
                    "data": notif.data,
                    "created_at": str(notif.created_at)
                }
            }
        )

        return Response({"status": "broadcasted", "id": notif.id})

