from .payment_processor import PaymentProcessor


class UPIPayment(PaymentProcessor):
    method_name = "UPI"

    def validate_reference(self, reference: str) -> bool:
        return "@" in reference and len(reference) >= 5