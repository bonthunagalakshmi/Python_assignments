from abc import ABC, abstractmethod

from exceptions.rental_exceptions import ValidationError


class Vehicle(ABC):
    """Abstract fleet vehicle with validated, encapsulated core fields."""

    VALID_STATUSES = {"AVAILABLE", "RESERVED", "RENTED", "MAINTENANCE"}

    def __init__(
        self,
        vehicle_id: str,
        registration_number: str,
        brand: str,
        model: str,
        year: int,
        fuel_type: str,
        transmission: str,
        seats: int,
        daily_rate: float,
        odometer: int = 0,
        fuel_level: float = 100,
        condition: str = "GOOD",
        status: str = "AVAILABLE",
    ):
        self.vehicle_id = self._required(vehicle_id, "Vehicle ID")
        self.registration_number = self._required(registration_number, "Registration number").upper()
        self.brand = self._required(brand, "Brand")
        self.model = self._required(model, "Model")
        self.year = int(year)
        self.fuel_type = self._required(fuel_type, "Fuel type")
        self.transmission = self._required(transmission, "Transmission")
        self.seats = int(seats)
        self.daily_rate = float(daily_rate)
        self.odometer = int(odometer)
        self.fuel_level = float(fuel_level)
        self.condition = self._required(condition, "Condition")
        self.status = status.upper()
        if self.year < 1900 or self.seats < 1 or self.daily_rate <= 0:
            raise ValidationError("Vehicle year, seats, and daily rate must be valid.")
        if not 0 <= self.fuel_level <= 100:
            raise ValidationError("Fuel level must be between 0 and 100.")
        if self.status not in self.VALID_STATUSES:
            raise ValidationError(f"Unknown vehicle status: {status}.")

    @staticmethod
    def _required(value: object, label: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValidationError(f"{label} is required.")
        return text

    @property
    def vehicle_type(self) -> str:
        return self.__class__.__name__.upper()

    def set_status(self, status: str) -> None:
        status = status.upper().strip()
        if status not in self.VALID_STATUSES:
            raise ValidationError(f"Unknown vehicle status: {status}.")
        self.status = status

    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        """Calculate the base rental amount for a number of days."""

    def to_record(self) -> dict[str, object]:
        return {
            "vehicle_id": self.vehicle_id,
            "registration_number": self.registration_number,
            "vehicle_type": self.vehicle_type.title(),
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "seats": self.seats,
            "daily_rate": round(self.daily_rate, 2),
            "odometer": self.odometer,
            "fuel_level": round(self.fuel_level, 2),
            "condition": self.condition,
            "status": self.status,
        }