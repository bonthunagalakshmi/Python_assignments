from datetime import date

from data.excel_manager import ExcelManager
from exceptions.rental_exceptions import CustomerNotFoundError, ValidationError
from models.customer import Customer
from utils.id_generator import next_identifier
from utils.validators import clean_text


class CustomerService:
    def __init__(self, excel: ExcelManager):
        self.excel = excel

    def list_customers(self) -> list[dict[str, object]]:
        return self.excel.read_records("Customers")

    def get_customer(self, customer_id: str) -> Customer:
        for record in self.list_customers():
            if record["customer_id"] == customer_id:
                return Customer(**record)
        raise CustomerNotFoundError(f"Customer {customer_id} was not found.")

    def create_customer(
        self, name: str, email: str, phone: str, driving_licence: str, address: str
    ) -> Customer:
        name = clean_text(name, "Name")
        driving_licence = clean_text(driving_licence, "Driving licence")
        address = clean_text(address, "Address")
        customer_id = next_identifier("CUS", (r["customer_id"] for r in self.list_customers()))
        customer = Customer(
            customer_id, name, email, phone, driving_licence, address, date.today().isoformat()
        )
        self.excel.append_record("Customers", customer.to_record())
        return customer

    def search_customers(self, query: str) -> list[dict[str, object]]:
        query = query.lower().strip()
        if not query:
            return self.list_customers()
        return [
            row for row in self.list_customers()
            if query in " ".join(str(value) for value in row.values()).lower()
        ]