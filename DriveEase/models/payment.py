from dataclasses import dataclass


@dataclass
class Payment:
    payment_id: str
    rental_id: str
    amount: float
    payment_method: str
    payment_date: str
    status: str
    reference_id: str = ""

    def to_record(self) -> dict[str, object]:
        return self.__dict__.copy()