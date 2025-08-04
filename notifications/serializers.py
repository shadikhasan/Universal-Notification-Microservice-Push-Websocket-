# notifications/serializers.py
from rest_framework import serializers

class NotificationSendSerializer(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)

