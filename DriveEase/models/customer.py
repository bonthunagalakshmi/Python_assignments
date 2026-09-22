from dataclasses import dataclass
from datetime import date

from exceptions.rental_exceptions import ValidationError
from utils.validators import validate_email, validate_phone


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    driving_licence: str
    address: str
    registration_date: str
    status: str = "ACTIVE"

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.driving_licence.strip() or not self.address.strip():
            raise ValidationError("Name, driving licence, and address are required.")
        self.email = validate_email(self.email)
        self.phone = validate_phone(self.phone)
        self.status = self.status.upper()

    def to_record(self) -> dict[str, str]:
        return self.__dict__.copy()