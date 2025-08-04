from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from .models import Tenant
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            query_string = parse_qs(self.scope["query_string"].decode())
            api_key = query_string.get("api_key", [None])[0]

            if not api_key:
                logger.warning("Missing API key on WebSocket connect.")
                await self.close()
                return

            try:
                self.tenant = await Tenant.objects.aget(api_key=api_key)
            except ObjectDoesNotExist:
                logger.warning(f"Invalid API key used: {api_key}")
                await self.close()
                return

            self.group_name = f"tenant_{self.tenant.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            logger.info(f"[WS CONNECTED] Tenant {self.tenant.name} joined {self.group_name}")

        except Exception as e:
            logger.exception(f"[WS ERROR] During connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "group_name"):
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
                logger.info(f"[WS DISCONNECTED] Left group {self.group_name}")
        except Exception as e:
            logger.exception(f"[WS ERROR] During disconnect: {str(e)}")

    async def notify(self, event):
        try:
            await self.send(text_data=json.dumps(event["data"]))
        except Exception as e:
            logger.exception(f"[WS ERROR] Sending message: {str(e)}")
