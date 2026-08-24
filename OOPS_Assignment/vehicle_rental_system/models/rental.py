from datetime import date
from exceptions.rental_exceptions import InvalidRentalDaysError

class Rental:

    def __init__(self, rental_id, customer, vehicle, days):
        self.__rental_id = rental_id
        self.__customer = customer
        self.__vehicle = vehicle
        self.__days = days
        self.__rental_date = date.today()
        self.__return_date = None
        self.__total_amount = 0
        self.__status = "Active"

        self.__payment_processor = None
        self.__invoice = None

        self.__validate_rental()
        

    def __validate_rental(self):
        if not self.__rental_id:
            raise ValueError("Rental ID cannot be empty.")

        if self.__customer is None:
            raise ValueError("Customer is required.")

        if self.__vehicle is None:
            raise ValueError("Vehicle is required.")

        if self.__days <= 0:
            raise InvalidRentalDaysError(
                "Rental days must be greater than zero."
            )

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def customer(self):
        return self.__customer

    @property
    def vehicle(self):
        return self.__vehicle

    @property
    def days(self):
        return self.__days

    @property
    def rental_date(self):
        return self.__rental_date

    @property
    def return_date(self):
        return self.__return_date

    @property
    def total_amount(self):
        return self.__total_amount

    @property
    def status(self):
        return self.__status

    def calculate_final_amount(self):
        self.__total_amount = self.__vehicle.calculate_rental_cost(
            self.__days
        )

        return self.__total_amount

    def complete_rental(self, return_date=None):
        if self.__status != "Active":
            raise ValueError("Rental is already completed.")

        if return_date is None:
            return_date = date.today()

        self.__return_date = return_date
        self.__status = "Completed"

        self.__vehicle.mark_as_available()

    def __str__(self):
        return (
            f"Rental ID: {self.__rental_id} | "
            f"Vehicle: {self.__vehicle.vehicle_id} | "
            f"Days: {self.__days} | "
            f"Amount: Rs. {self.__total_amount:.2f} | "
            f"Status: {self.__status}"
        )

    def set_payment_processor(self, payment_processor):
        self.__payment_processor = payment_processor

    def set_invoice(self, invoice):
        self.__invoice = invoice

    @property
    def payment_processor(self):
        return self.__payment_processor

    @property
    def invoice(self):
        return self.__invoice
