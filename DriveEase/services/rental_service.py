from __future__ import annotations

from datetime import date

from data.excel_manager import ExcelManager
from exceptions.rental_exceptions import (
    CustomerNotFoundError,
    InvalidRentalPeriodError,
    RentalNotFoundError,
    ValidationError,
    VehicleUnavailableError,
)
from models.invoice import Invoice
from models.rental import Rental
from services.customer_service import CustomerService
from services.fleet_service import FleetService
from services.payment_service import PaymentService
from services.pricing_service import PricingService
from utils.id_generator import next_identifier
from utils.validators import as_date, as_float, as_int


class RentalService:
    ACTIVE_BOOKING_STATUSES = {"CONFIRMED", "ACTIVE"}

    def __init__(
        self,
        excel: ExcelManager,
        customers: CustomerService,
        fleet: FleetService,
        pricing: PricingService | None = None,
        payments: PaymentService | None = None,
    ):
        self.excel = excel
        self.customers = customers
        self.fleet = fleet
        self.pricing = pricing or PricingService()
        self.payments = payments or PaymentService(excel)

    def list_rentals(self) -> list[dict[str, object]]:
        return self.excel.read_records("Rentals")

    def get_rental(self, rental_id: str) -> dict[str, object]:
        for rental in self.list_rentals():
            if rental["rental_id"] == rental_id:
                return rental
        raise RentalNotFoundError(f"Rental {rental_id} was not found.")

    @staticmethod
    def _ensure_period(pickup_date: str, return_date: str) -> tuple[date, date]:
        pickup = as_date(pickup_date, "Pickup date")
        returned = as_date(return_date, "Return date")
        if returned <= pickup:
            raise InvalidRentalPeriodError("Return date must be after pickup date.")
        return pickup, returned

    def is_vehicle_available(self, vehicle_id: str, pickup_date: str, return_date: str) -> bool:
        pickup, returned = self._ensure_period(pickup_date, return_date)
        vehicle = self.fleet.get_vehicle(vehicle_id)
        if vehicle.status == "MAINTENANCE":
            return False
        for rental in self.list_rentals():
            if rental["vehicle_id"] != vehicle_id or rental["status"] not in self.ACTIVE_BOOKING_STATUSES:
                continue
            existing_start = as_date(rental["pickup_date"])
            existing_end = as_date(rental["return_date"])
            # Start-inclusive/end-exclusive: touching boundaries are allowed.
            if existing_start < returned and pickup < existing_end:
                return False
        return True

    def available_vehicles(self, pickup_date: str, return_date: str) -> list[dict[str, object]]:
        self._ensure_period(pickup_date, return_date)
        return [
            record for record in self.fleet.list_records()
            if self.is_vehicle_available(str(record["vehicle_id"]), pickup_date, return_date)
        ]

    def create_quotation(
        self,
        customer_id: str,
        vehicle_id: str,
        pickup_date: str,
        return_date: str,
        discount: float = 0,
    ) -> dict[str, object]:
        self.customers.get_customer(customer_id)
        vehicle = self.fleet.get_vehicle(vehicle_id)
        if not self.is_vehicle_available(vehicle_id, pickup_date, return_date):
            raise VehicleUnavailableError(f"Vehicle {vehicle_id} is not available for those dates.")
        quote = self.pricing.quote(vehicle, pickup_date, return_date, discount)
        return {
            "customer_id": customer_id, "vehicle_id": vehicle_id,
            "pickup_date": pickup_date, "return_date": return_date, **quote,
        }

    def save_quotation(
        self,
        customer_id: str,
        vehicle_id: str,
        pickup_date: str,
        return_date: str,
        discount: float = 0,
    ) -> Rental:
        """Persist a quote without taking payment; staff may cancel it before confirmation."""
        quote = self.create_quotation(customer_id, vehicle_id, pickup_date, return_date, discount)
        rental_id = next_identifier("RNT", (r["rental_id"] for r in self.list_rentals()))
        rental = Rental(
            rental_id=rental_id,
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            pickup_date=pickup_date,
            return_date=return_date,
            base_amount=float(quote["base_amount"]),
            discount=float(quote["discount"]),
            tax=float(quote["tax"]),
            final_amount=float(quote["final_amount"]),
            status="QUOTED",
            created_date=date.today().isoformat(),
            pickup_odometer=self.fleet.get_vehicle(vehicle_id).odometer,
            pickup_fuel_level=self.fleet.get_vehicle(vehicle_id).fuel_level,
            pickup_condition=self.fleet.get_vehicle(vehicle_id).condition,
        )
        self.excel.append_record("Rentals", rental.to_record())
        return rental

    def confirm_rental(
        self,
        customer_id: str,
        vehicle_id: str,
        pickup_date: str,
        return_date: str,
        payment_method: str,
        payment_reference: str = "",
        payment_amount: float | None = None,
        discount: float = 0,
    ) -> tuple[Rental, Invoice, object]:
        self.customers.get_customer(customer_id)
        vehicle = self.fleet.get_vehicle(vehicle_id)
        quote = self.create_quotation(customer_id, vehicle_id, pickup_date, return_date, discount)
        amount = quote["final_amount"] if payment_amount is None else as_float(payment_amount, "Payment amount", 0.01)
        if amount > float(quote["final_amount"]):
            raise ValidationError("Payment cannot exceed the quoted amount.")
        # Validate before writing any rental, invoice, or payment records.
        payment_result = self.payments.validate_payment(amount, payment_method, payment_reference)
        rental_id = next_identifier("RNT", (r["rental_id"] for r in self.list_rentals()))
        rental = Rental(
            rental_id=rental_id,
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            pickup_date=pickup_date,
            return_date=return_date,
            base_amount=float(quote["base_amount"]),
            discount=float(quote["discount"]),
            tax=float(quote["tax"]),
            final_amount=float(quote["final_amount"]),
            status="CONFIRMED",
            created_date=date.today().isoformat(),
            pickup_odometer=int(vehicle.odometer),
            pickup_fuel_level=float(vehicle.fuel_level),
            pickup_condition=vehicle.condition,
        )
        self.excel.append_record("Rentals", rental.to_record())
        payment = self.payments.record_payment(rental_id, payment_result)
        invoice = self._create_invoice(rental)
        self._refresh_invoice(rental_id)
        self._sync_statuses()
        invoice = self.get_invoice_for_rental(rental_id)
        return rental, invoice, payment

    def _create_invoice(self, rental: Rental) -> Invoice:
        invoice_id = next_identifier("INV", (r["invoice_id"] for r in self.excel.read_records("Invoices")))
        invoice = Invoice(
            invoice_id, rental.rental_id, rental.customer_id, rental.vehicle_id,
            rental.base_amount, rental.additional_charges, rental.discount, rental.tax,
            rental.final_amount, 0, rental.final_amount, "UNPAID", date.today().isoformat(),
        )
        self.excel.append_record("Invoices", invoice.to_record())
        return invoice

    def get_invoice_for_rental(self, rental_id: str) -> dict[str, object]:
        invoice = next((r for r in self.excel.read_records("Invoices") if r["rental_id"] == rental_id), None)
        if invoice is None:
            raise RentalNotFoundError(f"Invoice for rental {rental_id} was not found.")
        return invoice

    def _refresh_invoice(self, rental_id: str) -> dict[str, object]:
        invoice = self.get_invoice_for_rental(rental_id)
        rental = self.get_rental(rental_id)
        paid = self.payments.total_paid(rental_id)
        total = float(rental["final_amount"])
        due = round(max(0, total - paid), 2)
        status = "PAID" if due == 0 else ("PARTIAL" if paid > 0 else "UNPAID")
        self.excel.update_record("Invoices", "invoice_id", invoice["invoice_id"], {
            "base_amount": rental["base_amount"],
            "additional_charges": rental["additional_charges"],
            "discount": rental["discount"],
            "tax": rental["tax"],
            "total": total,
            "amount_paid": paid,
            "amount_due": due,
            "payment_status": status,
        })
        return self.get_invoice_for_rental(rental_id)

    def collect_payment(
        self, rental_id: str, amount: float, method: str, reference_id: str = ""
    ) -> tuple[object, dict[str, object]]:
        rental = self.get_rental(rental_id)
        invoice = self.get_invoice_for_rental(rental_id)
        due = float(invoice["amount_due"])
        amount = as_float(amount, "Payment amount", 0.01)
        if amount > due:
            raise ValidationError("Payment cannot exceed the outstanding balance.")
        payment = self.payments.process_payment(rental_id, amount, method, reference_id)
        return payment, self._refresh_invoice(rental_id)

    def return_vehicle(
        self,
        rental_id: str,
        actual_return_date: str,
        return_odometer: int,
        return_fuel_level: float,
        return_condition: str,
        return_remarks: str = "",
        send_to_maintenance: bool = False,
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        rental = self.get_rental(rental_id)
        if rental["status"] not in self.ACTIVE_BOOKING_STATUSES:
            raise ValidationError("Only confirmed or active rentals can be returned.")
        vehicle = self.fleet.get_vehicle(str(rental["vehicle_id"]))
        actual = as_date(actual_return_date, "Actual return date")
        scheduled = as_date(rental["return_date"], "Scheduled return date")
        if actual < as_date(rental["pickup_date"], "Pickup date"):
            raise InvalidRentalPeriodError("Actual return cannot be before pickup.")
        return_fuel = as_float(return_fuel_level, "Return fuel level", 0)
        if return_fuel > 100:
            raise ValidationError("Return fuel level must be between 0 and 100.")
        charges = self.pricing.calculate_return_charges(
            vehicle, scheduled, actual, float(rental["pickup_fuel_level"]),
            return_fuel, return_condition, return_remarks,
        )
        updated = {
            "actual_return_date": actual.isoformat(),
            "additional_charges": float(charges["total"]),
            "tax": self.pricing.quote(
                vehicle, rental["pickup_date"], rental["return_date"],
                float(rental["discount"]), float(charges["total"]),
            )["tax"],
            "final_amount": self.pricing.quote(
                vehicle, rental["pickup_date"], rental["return_date"],
                float(rental["discount"]), float(charges["total"]),
            )["final_amount"],
            "status": "COMPLETED",
            "return_odometer": as_int(return_odometer, "Return odometer", 0),
            "return_fuel_level": return_fuel,
            "return_condition": str(return_condition).strip() or "GOOD",
            "return_remarks": str(return_remarks or "").strip(),
            "charge_breakdown": (
                f"Late: {charges['late_fee']:.2f}; Fuel: {charges['fuel_charge']:.2f}; "
                f"Damage: {charges['damage_charge']:.2f}"
            ),
        }
        self.excel.update_record("Rentals", "rental_id", rental_id, updated)
        self.fleet.update_vehicle(
            str(rental["vehicle_id"]),
            odometer=updated["return_odometer"],
            fuel_level=return_fuel,
            condition=updated["return_condition"],
            status="MAINTENANCE" if send_to_maintenance else "AVAILABLE",
        )
        invoice = self._refresh_invoice(rental_id)
        return self.get_rental(rental_id), invoice, charges

    def cancel_rental(self, rental_id: str) -> dict[str, object]:
        rental = self.get_rental(rental_id)
        if rental["status"] not in {"QUOTED", "CONFIRMED"}:
            raise ValidationError("Only quoted or confirmed rentals can be cancelled.")
        if self.payments.total_paid(rental_id) > 0:
            raise ValidationError("Refunds are outside this simulation; paid rentals cannot be cancelled.")
        self.excel.update_record("Rentals", "rental_id", rental_id, {"status": "CANCELLED"})
        self._sync_statuses()
        return self.get_rental(rental_id)

    def _sync_statuses(self) -> None:
        today = date.today().isoformat()
        rentals = self.list_rentals()
        for rental in rentals:
            if rental["status"] == "CONFIRMED" and str(rental["pickup_date"]) <= today < str(rental["return_date"]):
                self.excel.update_record("Rentals", "rental_id", rental["rental_id"], {"status": "ACTIVE"})
            elif rental["status"] == "ACTIVE" and not (str(rental["pickup_date"]) <= today < str(rental["return_date"])):
                self.excel.update_record("Rentals", "rental_id", rental["rental_id"], {"status": "CONFIRMED"})
        self.fleet.sync_operational_statuses(self.list_rentals(), today)