# Employee Management System

## Overview

This assignment demonstrates Python modules, packages, third-party libraries, virtual environments, dependency management, and dependency isolation.

The assignment contains two independent projects:

1. HR Report Generator
2. Employee CLI

Both projects use an `employee_system` package containing employee-related modules.

---

# 1. Python Modules

A module is a Python file containing related code.

The `employee_system` package contains:

- `employee.py` - employee-related functions
- `salary.py` - salary-related functions
- `attendance.py` - attendance-related functions

Example:

```python
from employee_system.employee import get_all_employees
