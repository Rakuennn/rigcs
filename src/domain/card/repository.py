import logging
from datetime import datetime, timezone
from typing import Optional

from google.cloud.firestore_v1.base_document import DocumentSnapshot

from config.settings import settings
from data.firebase.client import get_db
from domain.card.exceptions import FirebaseUnavailableException

logger = logging.getLogger(__name__)


class CardRepository:
    def get_card(self, card_id: str) -> Optional[dict]:
        """Fetch a card document. Returns dict or None if not found."""
        try:
            db = get_db()
            doc: DocumentSnapshot = (
                db.collection(settings.CARDS_COLLECTION).document(card_id).get()
            )
            return doc.to_dict() if doc.exists else None
        except Exception as exc:
            logger.error("Firestore get_card failed: card_id=%s error=%s", card_id, exc)
            raise FirebaseUnavailableException()

    def write_access_log(self, card_id: str, granted: bool, message: str) -> None:
        """Append access log. Fire-and-forget — errors are logged, not raised."""
        try:
            db = get_db()
            db.collection(settings.ACCESS_LOGS_COLLECTION).add(
                {
                    "card_id": card_id,
                    "timestamp": datetime.now(tz=timezone.utc),
                    "granted": granted,
                    "message": message,
                }
            )
        except Exception as exc:
            logger.error("Firestore write_access_log failed: card_id=%s error=%s", card_id, exc)

    def register_card(self, card_id: str, owner_name: str) -> None:
        """Create a new card document. Caller ensures no duplicate exists."""
        try:
            db = get_db()
            now = datetime.now(tz=timezone.utc)
            db.collection(settings.CARDS_COLLECTION).document(card_id).set(
                {
                    "is_master": False,
                    "owner_name": owner_name,
                    "isDelete": False,
                    "createDate": now,
                    "updateDate": now,
                }
            )
        except Exception as exc:
            logger.error("Firestore register_card failed: card_id=%s error=%s", card_id, exc)
            raise FirebaseUnavailableException()

    def grant_master_card(self, card_id: str) -> None:
        """Elevate card to master. Caller ensures card exists and is not already master."""
        try:
            db = get_db()
            db.collection(settings.CARDS_COLLECTION).document(card_id).update(
                {
                    "is_master": True,
                    "updateDate": datetime.now(tz=timezone.utc),
                }
            )
        except Exception as exc:
            logger.error("Firestore grant_master_card failed: card_id=%s error=%s", card_id, exc)
            raise FirebaseUnavailableException()
