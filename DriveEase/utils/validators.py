import re
from datetime import date, datetime
from typing import Any

from exceptions.rental_exceptions import ValidationError


def clean_text(value: Any, field: str, required: bool = True) -> str:
    text = str(value or "").strip()
    if required and not text:
        raise ValidationError(f"{field} is required.")
    return text


def as_date(value: Any, field: str = "Date") -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must use YYYY-MM-DD format.") from exc


def as_float(value: Any, field: str, minimum: float | None = None) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be a number.") from exc
    if minimum is not None and number < minimum:
        raise ValidationError(f"{field} must be at least {minimum}.")
    return round(number, 2)


def as_int(value: Any, field: str, minimum: int | None = None) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be a whole number.") from exc
    if minimum is not None and number < minimum:
        raise ValidationError(f"{field} must be at least {minimum}.")
    return number


def validate_email(value: Any) -> str:
    email = clean_text(value, "Email")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValidationError("Enter a valid email address.")
    return email.lower()


def validate_phone(value: Any) -> str:
    phone = clean_text(value, "Phone")
    if not re.fullmatch(r"[0-9+() -]{7,20}", phone):
        raise ValidationError("Enter a valid phone number.")
    return phone