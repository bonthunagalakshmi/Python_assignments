from abc import ABC, abstractmethod
from exceptions.rental_exceptions import VehicleUnavailableError

class Vehicle(ABC):

    def __init__(
        self,
        vehicle_id,
        registration_number,
        brand,
        model,
        daily_rate
    ):
        self.__vehicle_id = vehicle_id
        self.__registration_number = registration_number
        self.__brand = brand
        self.__model = model
        self.__daily_rate = daily_rate
        self.__available = True

        self.__validate_vehicle()

    def __validate_vehicle(self):
        if not self.__vehicle_id:
            raise ValueError("Vehicle ID cannot be empty.")

        if not self.__registration_number:
            raise ValueError("Registration number cannot be empty.")

        if not self.__brand:
            raise ValueError("Brand cannot be empty.")

        if not self.__model:
            raise ValueError("Model cannot be empty.")

        if self.__daily_rate <= 0:
            raise ValueError("Daily rental rate must be greater than zero.")

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def registration_number(self):
        return self.__registration_number

    @property
    def brand(self):
        return self.__brand

    @property
    def model(self):
        return self.__model

    @property
    def daily_rate(self):
        return self.__daily_rate

    @property
    def available(self):
        return self.__available

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass

    def display_details(self):
        status = "Available" if self.__available else "Rented"

        print(
            f"{self.__vehicle_id} | "
            f"{self.__class__.__name__} | "
            f"{self.__brand} | "
            f"{self.__model} | "
            f"Rs. {self.__daily_rate:.2f}/day | "
            f"{status}"
        )

    def mark_as_rented(self):
        if not self.__available:
            raise VehicleUnavailableError(
                f"Vehicle {self.__vehicle_id} is unavailable."
            )
        self.__available = False

    def mark_as_available(self):
        self.__available = True