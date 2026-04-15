import firebase_admin
from firebase_admin import credentials, firestore

from config.settings import settings

_db = None


def init_firebase() -> None:
    """Initialize Firebase app (idempotent — safe to call multiple times)."""
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)


def get_db() -> firestore.Client:
    """Return a Firestore client (lazy singleton)."""
    global _db
    if _db is None:
        _db = firestore.client(database_id=settings.FIRESTORE_DATABASE)
    return _db
