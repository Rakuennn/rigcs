import json
import logging
import threading

import paho.mqtt.client as mqtt

from config.settings import settings
from mqtt.topics import Topics

logger = logging.getLogger(__name__)


class MQTTClient:
    """
    Singleton MQTT client.
    Call start() on app startup and stop() on shutdown.
    """

    def __init__(self):
        self._client = mqtt.Client(
            client_id=settings.MQTT_CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        self._thread: threading.Thread | None = None
        self._on_message_cb = None

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        if settings.MQTT_USERNAME:
            self._client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def set_message_callback(self, callback) -> None:
        """Register handler: callback(topic: str, payload: dict) -> None"""
        self._on_message_cb = callback

    def start(self) -> None:
        logger.info("[MQTT] Connecting to %s:%s …", settings.MQTT_BROKER, settings.MQTT_PORT)
        self._client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)
        self._thread = threading.Thread(target=self._client.loop_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        logger.info("[MQTT] Disconnecting …")
        self._client.disconnect()

    def publish(self, topic: str, payload: dict, qos: int = 1) -> None:
        message = json.dumps(payload, default=str)
        self._client.publish(topic, message, qos=qos)
        logger.debug("[MQTT] → %s | %s", topic, message)

    # ── Paho callbacks ────────────────────────────────────────────────────────

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("[MQTT] ✅ Connected to broker")
            client.subscribe(Topics.CMD_ALL, qos=1)
            logger.info("[MQTT] Subscribed → %s", Topics.CMD_ALL)
        else:
            logger.error("[MQTT] ❌ Connection failed reason_code=%s", reason_code)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        logger.warning("[MQTT] Disconnected reason_code=%s", reason_code)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception as exc:
            logger.error("[MQTT] Bad payload on %s: %s", msg.topic, exc)
            return

        logger.info("[MQTT] ← %s | %s", msg.topic, payload)

        if self._on_message_cb:
            try:
                self._on_message_cb(msg.topic, payload)
            except Exception as exc:
                logger.exception("[MQTT] Handler error on %s: %s", msg.topic, exc)


mqtt_client = MQTTClient()
