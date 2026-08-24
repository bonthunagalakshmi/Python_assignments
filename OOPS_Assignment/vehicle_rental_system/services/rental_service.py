from models.rental import Rental
from models.invoice import Invoice

from exceptions.rental_exceptions import (
    InvalidRentalDaysError,
    VehicleUnavailableError,
    PaymentFailedError
)


class RentalService:

    def create_rental(
        self,
        rental_id,
        customer,
        vehicle,
        days,
        payment_processor
    ):

        if days <= 0:
            raise InvalidRentalDaysError(
                "Rental days must be greater than zero."
            )

        if not vehicle.available:
            raise VehicleUnavailableError(
                f"Vehicle {vehicle.vehicle_id} is unavailable."
            )

        amount = vehicle.calculate_rental_cost(days)

        # Payment must succeed before rental confirmation
        payment_success = payment_processor.process_payment(amount)

        if not payment_success:
            raise PaymentFailedError(
                "Payment failed. Rental cannot be confirmed."
            )

        # Vehicle becomes rented only after successful payment
        vehicle.mark_as_rented()

        rental = Rental(
            rental_id,
            customer,
            vehicle,
            days
        )

        rental.calculate_final_amount()

        # Store payment method inside Rental
        rental.set_payment_processor(payment_processor)

        # Create invoice as part of rental workflow
        invoice = Invoice(rental)
        rental.set_invoice(invoice)

        customer.add_rental(rental)

        return rental

    def return_vehicle(self, rental, return_date=None):

        if rental.status != "Active":
            raise ValueError(
                "Rental has already been completed."
            )

        rental.complete_rental(return_date)

        return rental

    def search_vehicles_by_type(self, vehicles, vehicle_type):

        results = []

        for vehicle in vehicles:

            if (
                vehicle.__class__.__name__.lower()
                == vehicle_type.lower()
                and vehicle.available
            ):
                results.append(vehicle)

        return results