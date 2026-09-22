from .payment_processor import PaymentProcessor


class CashPayment(PaymentProcessor):
    method_name = "CASH"

    def validate_reference(self, reference: str) -> bool:
        return not reference or reference.upper().startswith("CASH")