from datetime import date

from exceptions.rental_exceptions import InvalidRentalPeriodError, ValidationError
from models.vehicle import Vehicle
from utils.validators import as_date, as_float


class PricingService:
    TAX_RATE = 0.18
    FUEL_CHARGE_PER_PERCENT = 30.0
    DAMAGE_CHARGE = 3500.0

    def rental_days(self, pickup_date: str | date, return_date: str | date) -> int:
        pickup = as_date(pickup_date, "Pickup date")
        returned = as_date(return_date, "Return date")
        days = (returned - pickup).days
        if days <= 0:
            raise InvalidRentalPeriodError("Return date must be after pickup date.")
        return days

    def quote(
        self,
        vehicle: Vehicle,
        pickup_date: str | date,
        return_date: str | date,
        discount: float = 0,
        additional_charges: float = 0,
    ) -> dict[str, float | int]:
        days = self.rental_days(pickup_date, return_date)
        base_amount = vehicle.calculate_rental_cost(days)
        discount = as_float(discount, "Discount", 0)
        additional_charges = as_float(additional_charges, "Additional charges", 0)
        taxable = max(0, base_amount + additional_charges - discount)
        tax = round(taxable * self.TAX_RATE, 2)
        return {
            "days": days,
            "base_amount": round(base_amount, 2),
            "additional_charges": round(additional_charges, 2),
            "discount": round(discount, 2),
            "tax": tax,
            "final_amount": round(taxable + tax, 2),
        }

    def calculate_return_charges(
        self,
        vehicle: Vehicle,
        scheduled_return: str | date,
        actual_return: str | date,
        pickup_fuel: float,
        return_fuel: float,
        return_condition: str,
        damage_remarks: str = "",
    ) -> dict[str, float | int]:
        scheduled = as_date(scheduled_return, "Scheduled return date")
        actual = as_date(actual_return, "Actual return date")
        late_days = max(0, (actual - scheduled).days)
        late_fee = round(late_days * vehicle.daily_rate * 1.25, 2)
        shortage = max(0.0, float(pickup_fuel) - float(return_fuel))
        fuel_charge = round(shortage * self.FUEL_CHARGE_PER_PERCENT, 2)
        condition = str(return_condition).strip().upper()
        damage_charge = self.DAMAGE_CHARGE if condition in {"DAMAGED", "POOR"} or damage_remarks.strip() else 0.0
        return {
            "late_days": late_days,
            "late_fee": late_fee,
            "fuel_shortage": round(shortage, 2),
            "fuel_charge": fuel_charge,
            "damage_charge": damage_charge,
            "total": round(late_fee + fuel_charge + damage_charge, 2),
        }