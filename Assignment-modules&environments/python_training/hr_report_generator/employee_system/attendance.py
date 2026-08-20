attendance = {}


def mark_attendance(employee_id, status):
    if employee_id not in attendance:
        attendance[employee_id] = []

    attendance[employee_id].append(status)


def get_attendance(employee_id):
    return attendance.get(employee_id, [])


def calculate_attendance_percentage(employee_id):
    records = get_attendance(employee_id)

    if not records:
        return 0

    present_count = records.count("Present")

    return (present_count / len(records)) * 100