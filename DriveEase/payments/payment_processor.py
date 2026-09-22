from abc import ABC, abstractmethod
from dataclasses import dataclass

from exceptions.rental_exceptions import PaymentError
from utils.validators import as_float


@dataclass
class PaymentResult:
    amount: float
    method: str
    reference_id: str


class PaymentProcessor(ABC):
    method_name = "UNKNOWN"

    def process(self, amount: float, reference: str = "") -> PaymentResult:
        amount = as_float(amount, "Payment amount", minimum=0.01)
        reference = str(reference or "").strip()
        if not self.validate_reference(reference):
            raise PaymentError(f"Invalid {self.method_name} payment reference.")
        return PaymentResult(amount, self.method_name, reference)

    @abstractmethod
    def validate_reference(self, reference: str) -> bool:
        raise NotImplementedError