"""
RIGCS – RFID Access Control System
Entry point: initialises Firebase and starts the MQTT event loop.
"""
import logging
import signal
import sys
import time

from data.firebase.client import init_firebase
from mqtt.client import mqtt_client
from mqtt.handler import handle_message

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def run() -> None:
    init_firebase()
    logger.info("Firebase initialised.")

    mqtt_client.set_message_callback(handle_message)
    mqtt_client.start()

    logger.info("────────────────────────────────────────")
    logger.info("  RIGCS MQTT Server running")
    logger.info("  Press Ctrl+C to stop")
    logger.info("────────────────────────────────────────")

    # graceful shutdown on SIGINT / SIGTERM
    def _shutdown(sig, frame):
        logger.info("Shutting down …")
        mqtt_client.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    while True:
        time.sleep(1)