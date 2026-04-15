"""
Pure Python domain exceptions — ไม่มี FastAPI dependency
"""


class CardNotFoundException(Exception):
    def __init__(self, card_id: str):
        super().__init__(f"Card '{card_id}' not found in the system.")
        self.card_id = card_id


class CardAlreadyExistsException(Exception):
    def __init__(self, card_id: str):
        super().__init__(f"Card '{card_id}' is already registered.")
        self.card_id = card_id


class MasterCardCannotRegisterException(Exception):
    def __init__(self, card_id: str):
        super().__init__(f"Card '{card_id}' is a master card and cannot be registered as a regular card.")
        self.card_id = card_id


class CardIsAlreadyMasterException(Exception):
    def __init__(self, card_id: str):
        super().__init__(f"Card '{card_id}' is already a master card.")
        self.card_id = card_id


class FirebaseUnavailableException(Exception):
    def __init__(self):
        super().__init__("Firebase service is currently unavailable.")
