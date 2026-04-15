"""
Domain models as plain dataclasses — no framework dependency
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CardRequest:
    card_id: str

    def __post_init__(self):
        if not self.card_id.strip():
            raise ValueError("card_id must not be empty.")
        # normalize to uppercase (matches RFID format)
        object.__setattr__(self, "card_id", self.card_id.strip().upper())


@dataclass(frozen=True)
class RegisterCardRequest:
    card_id: str
    owner_name: str = ""

    def __post_init__(self):
        if not self.card_id.strip():
            raise ValueError("card_id must not be empty.")
        object.__setattr__(self, "card_id", self.card_id.strip().upper())


@dataclass(frozen=True)
class AccessResult:
    granted: bool
    message: str
    card_id: str
    timestamp: str


@dataclass(frozen=True)
class MasterCardResult:
    is_master: bool
    message: str
    card_id: str
    timestamp: str


@dataclass(frozen=True)
class RegisterResult:
    success: bool
    message: str
    card_id: str
    timestamp: str


@dataclass(frozen=True)
class GrantMasterResult:
    success: bool
    message: str
    card_id: str
    timestamp: str
