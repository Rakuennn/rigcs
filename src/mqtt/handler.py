import logging

from domain.card.exceptions import (
    CardAlreadyExistsException,
    CardIsAlreadyMasterException,
    CardNotFoundException,
    FirebaseUnavailableException,
    MasterCardCannotRegisterException,
)
from domain.card.models import RegisterCardRequest
from domain.card.repository import CardRepository
from domain.card.service import CardService
from mqtt.topics import Topics

logger = logging.getLogger(__name__)


def _make_service() -> CardService:
    return CardService(repository=CardRepository())


def handle_message(topic: str, payload: dict) -> None:
    """Route incoming MQTT command to the correct service method."""
    from mqtt.client import mqtt_client  # lazy import avoids circular

    service = _make_service()

    handlers = {
        Topics.CMD_ACCESS: _handle_access,
        Topics.CMD_MASTER: _handle_master,
        Topics.CMD_REGISTER: _handle_register,
    }

    handler = handlers.get(topic)
    if handler:
        handler(service, payload, mqtt_client)
    else:
        logger.warning("[Handler] Unknown topic: %s", topic)


# ── Individual command handlers ───────────────────────────────────────────────

def _handle_access(service: CardService, payload: dict, client) -> None:
    card_id = payload.get("card_id", "").strip()
    if not card_id:
        logger.error("[Handler] access: missing card_id")
        return
    try:
        result = service.check_access(card_id)
        client.publish(Topics.RESULT_ACCESS, {
            "card_id": result.card_id,
            "granted": result.granted,
            "message": result.message,
            "timestamp": result.timestamp,
        })
    except FirebaseUnavailableException as exc:
        logger.error("[Handler] access: %s", exc)
        client.publish(Topics.RESULT_ACCESS, {
            "card_id": card_id,
            "granted": False,
            "message": "Server error — please try again.",
        })


def _handle_master(service: CardService, payload: dict, client) -> None:
    card_id = payload.get("card_id", "").strip()
    if not card_id:
        logger.error("[Handler] master: missing card_id")
        return
    try:
        result = service.check_master_card(card_id)
        client.publish(Topics.RESULT_MASTER, {
            "card_id": result.card_id,
            "is_master": result.is_master,
            "message": result.message,
            "timestamp": result.timestamp,
        })
    except FirebaseUnavailableException as exc:
        logger.error("[Handler] master: %s", exc)
        client.publish(Topics.RESULT_MASTER, {
            "card_id": card_id,
            "is_master": False,
            "message": "Server error — please try again.",
        })


def _handle_register(service: CardService, payload: dict, client) -> None:
    card_id = payload.get("card_id", "").strip()
    if not card_id:
        logger.error("[Handler] register: missing card_id")
        return
    req = RegisterCardRequest(card_id=card_id, owner_name=payload.get("owner_name", ""))
    try:
        result = service.register_card(req)
        client.publish(Topics.RESULT_REGISTER, {
            "card_id": result.card_id,
            "success": result.success,
            "message": result.message,
            "timestamp": result.timestamp,
        })
    except (CardAlreadyExistsException, MasterCardCannotRegisterException, CardNotFoundException, CardIsAlreadyMasterException) as exc:
        logger.warning("[Handler] register failed: %s", exc)
        client.publish(Topics.RESULT_REGISTER, {
            "card_id": card_id,
            "success": False,
            "message": str(exc),
        })
    except FirebaseUnavailableException as exc:
        logger.error("[Handler] register: %s", exc)
        client.publish(Topics.RESULT_REGISTER, {
            "card_id": card_id,
            "success": False,
            "message": "Server error — please try again.",
        })
