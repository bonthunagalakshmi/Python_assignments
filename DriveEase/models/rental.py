from dataclasses import dataclass, field


@dataclass
class Rental:
    rental_id: str
    customer_id: str
    vehicle_id: str
    pickup_date: str
    return_date: str
    actual_return_date: str = ""
    base_amount: float = 0.0
    additional_charges: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    final_amount: float = 0.0
    status: str = "QUOTED"
    created_date: str = ""
    pickup_odometer: int = 0
    pickup_fuel_level: float = 100.0
    pickup_condition: str = "GOOD"
    pickup_remarks: str = ""
    return_odometer: int = 0
    return_fuel_level: float = 0.0
    return_condition: str = ""
    return_remarks: str = ""
    charge_breakdown: str = field(default="")

    def to_record(self) -> dict[str, object]:
        return self.__dict__.copy()