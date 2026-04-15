import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        "rigcs-24f3e-firebase-adminsdk-fbsvc-16a37640bb.json",
    )
    FIRESTORE_DATABASE: str = os.getenv("FIRESTORE_DATABASE", "rigcs-database")
    CARDS_COLLECTION: str = "cards"
    ACCESS_LOGS_COLLECTION: str = "access_logs"

    # MQTT
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "")
    MQTT_CLIENT_ID: str = os.getenv("MQTT_CLIENT_ID", "rigcs-server")

    def __init__(self):
        self.FIREBASE_CREDENTIALS_PATH = os.getenv(
            "FIREBASE_CREDENTIALS_PATH",
            "rigcs-24f3e-firebase-adminsdk-fbsvc-16a37640bb.json",
        )
        self.FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE", "rigcs-database")
        self.CARDS_COLLECTION = "cards"
        self.ACCESS_LOGS_COLLECTION = "access_logs"
        self.MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
        self.MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
        self.MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
        self.MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
        self.MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "rigcs-server")


settings = Settings()
