from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable

from employee_system.employee import get_all_employees


# -----------------------------
# Jinja2 Report
# -----------------------------

employees = get_all_employees()

environment = Environment(
    loader=FileSystemLoader("templates")
)

template = environment.get_template("employee_report.txt")

for employee in employees:
    report = template.render(employee=employee)
    print(report)


# -----------------------------
# PrettyTable
# -----------------------------

table = PrettyTable()

table.field_names = ["ID", "Name", "Department", "Salary"]

for employee in employees:
    table.add_row([
        employee["id"],
        employee["name"],
        employee["department"],
        employee["salary"]
    ])

print("Employee Table")
print("==============")
print(table)