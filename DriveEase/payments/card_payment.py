import re

from .payment_processor import PaymentProcessor


class CardPayment(PaymentProcessor):
    method_name = "CARD"

    def validate_reference(self, reference: str) -> bool:
        # Only a safe masked representation or token is accepted.
        return bool(re.fullmatch(r"(\*{4}\d{4}|TOKEN-[A-Za-z0-9-]{4,})", reference))