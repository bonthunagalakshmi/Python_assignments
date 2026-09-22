from collections import Counter, defaultdict

from data.excel_manager import ExcelManager


class ReportService:
    """Calculates live summaries from the workbook instead of storing report totals."""

    def __init__(self, excel: ExcelManager):
        self.excel = excel

    def dashboard_summary(self) -> dict[str, float | int]:
        vehicles = self.excel.read_records("Vehicles")
        rentals = self.excel.read_records("Rentals")
        payments = self.excel.read_records("Payments")
        statuses = Counter(str(v["status"]).upper() for v in vehicles)
        return {
            "total_vehicles": len(vehicles),
            "available": statuses["AVAILABLE"],
            "reserved": statuses["RESERVED"],
            "rented": statuses["RENTED"],
            "maintenance": statuses["MAINTENANCE"],
            "active_rentals": sum(r["status"] == "ACTIVE" for r in rentals),
            "revenue": round(sum(float(p["amount"]) for p in payments if p["status"] == "SUCCESS"), 2),
        }

    def most_rented_vehicles(self) -> list[dict[str, object]]:
        counts = Counter(r["vehicle_id"] for r in self.excel.read_records("Rentals")
                         if r["status"] != "CANCELLED")
        vehicles = {v["vehicle_id"]: v for v in self.excel.read_records("Vehicles")}
        return [
            {"vehicle_id": vehicle_id, "registration_number": vehicles.get(vehicle_id, {}).get("registration_number", ""),
             "rental_count": count}
            for vehicle_id, count in counts.most_common()
        ]

    def revenue_by_vehicle_type(self) -> dict[str, float]:
        vehicles = {r["vehicle_id"]: r for r in self.excel.read_records("Vehicles")}
        totals: defaultdict[str, float] = defaultdict(float)
        for payment in self.excel.read_records("Payments"):
            if payment["status"] == "SUCCESS":
                kind = str(vehicles.get(payment["rental_id"], {}).get("vehicle_type", "UNKNOWN"))
                rental = next((r for r in self.excel.read_records("Rentals") if r["rental_id"] == payment["rental_id"]), None)
                if rental:
                    kind = str(vehicles.get(rental["vehicle_id"], {}).get("vehicle_type", "UNKNOWN"))
                totals[kind] += float(payment["amount"])
        return {key: round(value, 2) for key, value in totals.items()}

    def revenue_by_payment_method(self) -> dict[str, float]:
        totals: defaultdict[str, float] = defaultdict(float)
        for payment in self.excel.read_records("Payments"):
            if payment["status"] == "SUCCESS":
                totals[str(payment["payment_method"])] += float(payment["amount"])
        return {key: round(value, 2) for key, value in totals.items()}

    def customer_spending(self) -> list[dict[str, object]]:
        totals: defaultdict[str, float] = defaultdict(float)
        for payment in self.excel.read_records("Payments"):
            if payment["status"] != "SUCCESS":
                continue
            rental = next((r for r in self.excel.read_records("Rentals") if r["rental_id"] == payment["rental_id"]), None)
            if rental:
                totals[str(rental["customer_id"])] += float(payment["amount"])
        customers = {r["customer_id"]: r["name"] for r in self.excel.read_records("Customers")}
        return [
            {"customer_id": cid, "name": customers.get(cid, "Unknown"), "spending": round(amount, 2)}
            for cid, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True)
        ]

    def customer_rental_history(self, customer_id: str) -> list[dict[str, object]]:
        return [r for r in self.excel.read_records("Rentals") if r["customer_id"] == customer_id]

    def utilization(self) -> list[dict[str, object]]:
        rentals = [r for r in self.excel.read_records("Rentals") if r["status"] != "CANCELLED"]
        counts = Counter(r["vehicle_id"] for r in rentals)
        return [{"vehicle_id": vehicle_id, "rentals": count} for vehicle_id, count in counts.most_common()]