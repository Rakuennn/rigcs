import logging
from datetime import datetime, timezone

from domain.card.exceptions import (
    CardAlreadyExistsException,
    CardIsAlreadyMasterException,
    CardNotFoundException,
    MasterCardCannotRegisterException,
)
from domain.card.models import (
    AccessResult,
    GrantMasterResult,
    MasterCardResult,
    RegisterCardRequest,
    RegisterResult,
)
from domain.card.repository import CardRepository

logger = logging.getLogger(__name__)


class CardService:
    def __init__(self, repository: CardRepository):
        self._repo = repository

    def check_access(self, card_id: str) -> AccessResult:
        """Verify card access and log the result."""
        now = datetime.now(tz=timezone.utc).isoformat()
        card = self._repo.get_card(card_id)

        if card is None or card.get("isDelete", False):
            message = "Card not registered" if card is None else "Card has been deleted"
            self._repo.write_access_log(card_id=card_id, granted=False, message=message)
            return AccessResult(
                granted=False,
                message="Access denied: card not registered.",
                card_id=card_id,
                timestamp=now,
            )

        self._repo.write_access_log(card_id=card_id, granted=True, message="Card registered")
        return AccessResult(
            granted=True,
            message="Access granted.",
            card_id=card_id,
            timestamp=now,
        )

    def check_master_card(self, card_id: str) -> MasterCardResult:
        """Return whether the card holds master privileges."""
        now = datetime.now(tz=timezone.utc).isoformat()
        card = self._repo.get_card(card_id)
        is_master = bool(card and card.get("is_master", False))
        return MasterCardResult(
            is_master=is_master,
            message="Master card detected." if is_master else "Not a master card.",
            card_id=card_id,
            timestamp=now,
        )

    def register_card(self, req: RegisterCardRequest) -> RegisterResult:
        """Register a new card. Raises on conflict or master-card attempt."""
        now = datetime.now(tz=timezone.utc).isoformat()
        existing = self._repo.get_card(req.card_id)

        if existing is not None:
            if existing.get("is_master", False):
                raise MasterCardCannotRegisterException(req.card_id)
            raise CardAlreadyExistsException(req.card_id)

        self._repo.register_card(card_id=req.card_id, owner_name=req.owner_name)
        return RegisterResult(
            success=True,
            message=f"Card '{req.card_id}' registered successfully.",
            card_id=req.card_id,
            timestamp=now,
        )

    def grant_master_card(self, card_id: str) -> GrantMasterResult:
        """Elevate card to master status. Raises if card missing or already master."""
        now = datetime.now(tz=timezone.utc).isoformat()
        card = self._repo.get_card(card_id)

        if card is None:
            raise CardNotFoundException(card_id)
        if card.get("is_master", False):
            raise CardIsAlreadyMasterException(card_id)

        self._repo.grant_master_card(card_id)
        return GrantMasterResult(
            success=True,
            message=f"Card '{card_id}' has been granted master card privileges.",
            card_id=card_id,
            timestamp=now,
        )
