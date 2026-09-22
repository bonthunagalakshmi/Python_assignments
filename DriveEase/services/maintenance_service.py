from datetime import date

from data.excel_manager import ExcelManager
from exceptions.rental_exceptions import MaintenanceError
from services.fleet_service import FleetService
from utils.id_generator import next_identifier
from utils.validators import as_float, clean_text


class MaintenanceService:
    def __init__(self, excel: ExcelManager, fleet: FleetService):
        self.excel = excel
        self.fleet = fleet

    def list_records(self) -> list[dict[str, object]]:
        return self.excel.read_records("Maintenance")

    def start_maintenance(self, vehicle_id: str, reason: str, cost: float = 0, notes: str = "") -> dict[str, object]:
        vehicle = self.fleet.get_vehicle(vehicle_id)
        if vehicle.status == "RENTED":
            raise MaintenanceError("A rented vehicle cannot enter maintenance before return.")
        if vehicle.status == "MAINTENANCE":
            raise MaintenanceError("Vehicle is already in maintenance.")
        record = {
            "maintenance_id": next_identifier("MNT", (r["maintenance_id"] for r in self.list_records())),
            "vehicle_id": vehicle_id,
            "date": date.today().isoformat(),
            "reason": clean_text(reason, "Maintenance reason"),
            "cost": as_float(cost, "Maintenance cost", 0),
            "notes": str(notes or "").strip(),
            "status": "OPEN",
        }
        self.excel.append_record("Maintenance", record)
        self.fleet.set_status(vehicle_id, "MAINTENANCE")
        return record

    def complete_maintenance(self, maintenance_id: str) -> dict[str, object]:
        records = self.list_records()
        record = next((r for r in records if r["maintenance_id"] == maintenance_id), None)
        if record is None:
            raise MaintenanceError(f"Maintenance record {maintenance_id} was not found.")
        if record["status"] == "COMPLETED":
            raise MaintenanceError("Maintenance is already completed.")
        self.excel.update_record("Maintenance", "maintenance_id", maintenance_id, {"status": "COMPLETED"})
        self.fleet.set_status(str(record["vehicle_id"]), "AVAILABLE")
        record["status"] = "COMPLETED"
        return record