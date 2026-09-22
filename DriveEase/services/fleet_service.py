from __future__ import annotations

from data.excel_manager import ExcelManager
from exceptions.rental_exceptions import ValidationError, VehicleNotFoundError
from models.bike import Bike
from models.car import Car
from models.van import Van
from models.vehicle import Vehicle
from utils.id_generator import next_identifier
from utils.validators import as_float, as_int, clean_text


VEHICLE_CLASSES = {"CAR": Car, "BIKE": Bike, "VAN": Van}


class FleetService:
    def __init__(self, excel: ExcelManager):
        self.excel = excel

    def list_records(self) -> list[dict[str, object]]:
        return self.excel.read_records("Vehicles")

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        for record in self.list_records():
            if record["vehicle_id"] == vehicle_id:
                return self._from_record(record)
        raise VehicleNotFoundError(f"Vehicle {vehicle_id} was not found.")

    def _from_record(self, record: dict[str, object]) -> Vehicle:
        kind = str(record["vehicle_type"]).upper()
        vehicle_class = VEHICLE_CLASSES.get(kind)
        if vehicle_class is None:
            raise ValidationError(f"Unsupported vehicle type: {record['vehicle_type']}.")
        return vehicle_class(
            vehicle_id=str(record["vehicle_id"]),
            registration_number=str(record["registration_number"]),
            brand=str(record["brand"]),
            model=str(record["model"]),
            year=as_int(record["year"], "Year"),
            fuel_type=str(record["fuel_type"]),
            transmission=str(record["transmission"]),
            seats=as_int(record["seats"], "Seats", 1),
            daily_rate=as_float(record["daily_rate"], "Daily rental rate", 0.01),
            odometer=as_int(record["odometer"], "Odometer", 0),
            fuel_level=as_float(record["fuel_level"], "Fuel level", 0),
            condition=str(record["condition"]),
            status=str(record["status"]),
        )

    def add_vehicle(
        self,
        vehicle_type: str,
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
    ) -> Vehicle:
        kind = clean_text(vehicle_type, "Vehicle type").upper()
        if kind not in VEHICLE_CLASSES:
            raise ValidationError("Vehicle type must be Car, Bike, or Van.")
        registration_number = clean_text(registration_number, "Registration number").upper()
        if any(str(row["registration_number"]).upper() == registration_number for row in self.list_records()):
            raise ValidationError("Registration number must be unique.")
        prefix = kind
        vehicle_id = next_identifier(prefix, (r["vehicle_id"] for r in self.list_records()))
        vehicle = VEHICLE_CLASSES[kind](
            vehicle_id, registration_number, clean_text(brand, "Brand"),
            clean_text(model, "Model"), as_int(year, "Year", 1900),
            clean_text(fuel_type, "Fuel type"), clean_text(transmission, "Transmission"),
            as_int(seats, "Seats", 1), as_float(daily_rate, "Daily rental rate", 0.01),
            as_int(odometer, "Odometer", 0), as_float(fuel_level, "Fuel level", 0),
            clean_text(condition, "Condition"), "AVAILABLE",
        )
        self.excel.append_record("Vehicles", vehicle.to_record())
        return vehicle

    def search(self, query: str = "", vehicle_type: str = "ALL", status: str = "ALL") -> list[dict[str, object]]:
        query = query.lower().strip()
        vehicle_type = vehicle_type.upper()
        status = status.upper()
        results = self.list_records()
        return [
            row for row in results
            if (not query or query in " ".join(str(v) for v in row.values()).lower())
            and (vehicle_type == "ALL" or str(row["vehicle_type"]).upper() == vehicle_type)
            and (status == "ALL" or str(row["status"]).upper() == status)
        ]

    def update_vehicle(self, vehicle_id: str, **updates: object) -> Vehicle:
        vehicle = self.get_vehicle(vehicle_id)
        if "status" in updates:
            vehicle.set_status(str(updates["status"]))
        if "odometer" in updates:
            vehicle.odometer = as_int(updates["odometer"], "Odometer", 0)
        if "fuel_level" in updates:
            vehicle.fuel_level = as_float(updates["fuel_level"], "Fuel level", 0)
            if vehicle.fuel_level > 100:
                raise ValidationError("Fuel level must be between 0 and 100.")
        if "condition" in updates:
            vehicle.condition = clean_text(updates["condition"], "Condition")
        self.excel.update_record("Vehicles", "vehicle_id", vehicle_id, vehicle.to_record())
        return vehicle

    def set_status(self, vehicle_id: str, status: str) -> Vehicle:
        return self.update_vehicle(vehicle_id, status=status)

    def sync_operational_statuses(self, rentals: list[dict[str, object]], today: str) -> None:
        """Reflect current active/future bookings without using status for availability."""
        for vehicle in self.list_records():
            if str(vehicle["status"]).upper() == "MAINTENANCE":
                continue
            relevant = [
                rental for rental in rentals
                if rental["vehicle_id"] == vehicle["vehicle_id"]
                and rental["status"] in {"CONFIRMED", "ACTIVE"}
            ]
            new_status = "AVAILABLE"
            for rental in relevant:
                if str(rental["pickup_date"]) <= today < str(rental["return_date"]):
                    new_status = "RENTED"
                    break
                if str(rental["pickup_date"]) > today:
                    new_status = "RESERVED"
            if str(vehicle["status"]).upper() != new_status:
                self.excel.update_record("Vehicles", "vehicle_id", vehicle["vehicle_id"], {"status": new_status})