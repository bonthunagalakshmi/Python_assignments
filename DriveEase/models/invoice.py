from dataclasses import dataclass


@dataclass
class Invoice:
    invoice_id: str
    rental_id: str
    customer_id: str
    vehicle_id: str
    base_amount: float
    additional_charges: float
    discount: float
    tax: float
    total: float
    amount_paid: float
    amount_due: float
    payment_status: str
    generated_date: str

    def to_record(self) -> dict[str, object]:
        return self.__dict__.copy()