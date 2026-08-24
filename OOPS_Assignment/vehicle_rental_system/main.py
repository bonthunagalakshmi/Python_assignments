from datetime import timedelta

from models.car import Car
from models.bike import Bike
from models.van import Van
from models.customer import Customer
from models.invoice import Invoice

from payments.card_payment import CardPayment
from payments.upi_payment import UPIPayment

from services.rental_service import RentalService

from exceptions.rental_exceptions import (
    VehicleUnavailableError
)


# --------------------------------------------------
# 1. Create vehicles
# --------------------------------------------------

car = Car(
    "V101",
    "KA01AB1234",
    "Toyota",
    "Innova",
    2000
)

bike = Bike(
    "V102",
    "KA02CD5678",
    "Yamaha",
    "FZ",
    700
)

van = Van(
    "V103",
    "KA03EF9012",
    "Tata",
    "Winger",
    3000,
    500
)

vehicles = [car, bike, van]
# --------------------------------------------------
# 2. Create customers
# --------------------------------------------------

customer_a = Customer(
    "C101",
    "Ananya Sharma",
    "ananya@example.com",
    "DL123456"
)

customer_b = Customer(
    "C102",
    "Rahul Kumar",
    "rahul@example.com",
    "DL789012"
)


# --------------------------------------------------
# 3. Create payment methods
# --------------------------------------------------

card_payment = CardPayment(
    "Ananya Sharma"
)

upi_payment = UPIPayment(
    "rahul@upi"
)


# --------------------------------------------------
# 4. Create rental service
# --------------------------------------------------

rental_service = RentalService()


# --------------------------------------------------
# 5. Display available vehicles
# --------------------------------------------------

print("\nAVAILABLE VEHICLES")
print("-" * 70)

car.display_details()
bike.display_details()
van.display_details()

print("\nSEARCH VEHICLES BY TYPE")
print("-" * 60)

available_cars = rental_service.search_vehicles_by_type(
    vehicles,
    "Car"
)

for vehicle in available_cars:
    vehicle.display_details()

# --------------------------------------------------
# 6. Customer A rents car for 3 days
# --------------------------------------------------

print("\nCUSTOMER A RENTAL")
print("-" * 70)

rental_a = rental_service.create_rental(
    "R101",
    customer_a,
    car,
    3,
    card_payment
)

print("Rental created successfully.")
print(rental_a)


# --------------------------------------------------
# 7. Customer B tries to rent same car
# --------------------------------------------------

print("\nCUSTOMER B ATTEMPT")
print("-" * 70)

try:
    rental_service.create_rental(
        "R102",
        customer_b,
        car,
        2,
        upi_payment
    )

except VehicleUnavailableError as error:
    print("Vehicle unavailable:", error)


# --------------------------------------------------
# 8. Return car one day late
# --------------------------------------------------

print("\nVEHICLE RETURN")
print("-" * 70)

planned_return_date = (
    rental_a.rental_date + timedelta(days=3)
)

actual_return_date = (
    planned_return_date + timedelta(days=1)
)

rental_service.return_vehicle(
    rental_a,
    actual_return_date
)

print("Vehicle returned successfully.")


# --------------------------------------------------
# 9. Calculate late days
# --------------------------------------------------

late_days = (
    actual_return_date - planned_return_date
).days

print("Late days:", late_days)


# --------------------------------------------------
# 10. Generate invoice
# --------------------------------------------------

invoice = Invoice(rental_a)

invoice.generate(
    late_days=late_days
)

invoice.display()


# --------------------------------------------------
# 11. Confirm vehicle available again
# --------------------------------------------------

print("\nVEHICLE STATUS AFTER RETURN")
print("-" * 70)

car.display_details()


# --------------------------------------------------
# 12. Display customer rental history
# --------------------------------------------------

customer_a.display_rental_history()