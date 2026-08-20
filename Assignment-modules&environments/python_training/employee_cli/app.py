from tabulate import tabulate
from rich.console import Console
from rich.table import Table

from employee_system.employee import get_all_employees


employees = get_all_employees()


# -----------------------------
# Tabulate Table
# -----------------------------

print("Employee List - Tabulate")
print("------------------------")

print(
    tabulate(
        employees,
        headers="keys",
        tablefmt="grid"
    )
)


# -----------------------------
# Rich Table
# -----------------------------

print("\nEmployee List - Rich")
print("--------------------")

console = Console()

table = Table(title="Employee Details")

table.add_column("ID", style="cyan", justify="center")
table.add_column("Name", style="green", justify="left")
table.add_column("Department", style="yellow", justify="left")
table.add_column("Salary", style="magenta", justify="right")

for employee in employees:
    table.add_row(
        employee["id"],
        employee["name"],
        employee["department"],
        str(employee["salary"])
    )

console.print(table)