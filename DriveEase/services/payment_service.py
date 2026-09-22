from datetime import date

from data.excel_manager import ExcelManager
from exceptions.rental_exceptions import PaymentError
from models.payment import Payment
from payments.card_payment import CardPayment
from payments.cash_payment import CashPayment
from payments.payment_processor import PaymentProcessor
from payments.upi_payment import UPIPayment
from utils.id_generator import next_identifier


class PaymentService:
    PROCESSORS: dict[str, type[PaymentProcessor]] = {
        "UPI": UPIPayment,
        "CARD": CardPayment,
        "CASH": CashPayment,
    }

    def __init__(self, excel: ExcelManager):
        self.excel = excel

    def process_payment(
        self, rental_id: str, amount: float, method: str, reference_id: str = ""
    ) -> Payment:
        result = self.validate_payment(amount, method, reference_id)
        return self.record_payment(rental_id, result)

    def validate_payment(self, amount: float, method: str, reference_id: str = ""):
        method = method.upper().strip()
        processor_class = self.PROCESSORS.get(method)
        if processor_class is None:
            raise PaymentError("Payment method must be UPI, CARD, or CASH.")
        return processor_class().process(amount, reference_id)

    def record_payment(self, rental_id: str, result) -> Payment:
        payment_id = next_identifier("PAY", (r["payment_id"] for r in self.excel.read_records("Payments")))
        payment = Payment(
            payment_id, rental_id, result.amount, result.method, date.today().isoformat(),
            "SUCCESS", result.reference_id,
        )
        self.excel.append_record("Payments", payment.to_record())
        return payment

    def list_payments(self) -> list[dict[str, object]]:
        return self.excel.read_records("Payments")

    def payments_for(self, rental_id: str) -> list[dict[str, object]]:
        return [r for r in self.list_payments() if r["rental_id"] == rental_id and r["status"] == "SUCCESS"]

    def total_paid(self, rental_id: str) -> float:
        return round(sum(float(r["amount"]) for r in self.payments_for(rental_id)), 2)