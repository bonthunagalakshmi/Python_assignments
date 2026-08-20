employees = [
    {
        "id": "E001",
        "name": "John",
        "department": "IT",
        "salary": 50000
    },
    {
        "id": "E002",
        "name": "Alice",
        "department": "HR",
        "salary": 45000
    },
    {
        "id": "E003",
        "name": "Bob",
        "department": "Finance",
        "salary": 55000
    }
]


def add_employee(employee):
    employees.append(employee)


def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def get_all_employees():
    return employees