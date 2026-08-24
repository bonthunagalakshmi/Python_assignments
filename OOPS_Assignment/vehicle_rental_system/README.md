# Vehicle Rental Management System

## 1. Project Description

The Vehicle Rental Management System is a console-based Python application
developed to demonstrate Object-Oriented Programming concepts through a
real-world vehicle rental scenario.

The system supports:

- Cars, bikes, and vans
- Customer registration
- Vehicle availability management
- Vehicle search by type
- Vehicle rental
- Card and UPI payment processing
- Rental returns
- Late-fee calculation
- Invoice generation
- Customer rental history
- Exception handling

The project is designed using separate classes and packages so that each
class has a focused responsibility and the system can be extended without
rewriting the complete application.

---

## 2. Project Objectives

The project demonstrates the following Object-Oriented Programming concepts:

- Classes and objects
- Encapsulation
- Abstraction
- Inheritance
- Polymorphism
- Method overriding
- Interfaces / contracts
- Composition
- Association
- Dependency inversion
- Exception handling

These concepts are applied to the vehicle rental business problem described
in the assignment.

---

## 3. Project Structure

```text
vehicle_rental_system/
│
├── main.py
├── README.md
├── class_diagram.png
│
├── models/
│   ├── __init__.py
│   ├── vehicle.py
│   ├── car.py
│   ├── bike.py
│   ├── van.py
│   ├── customer.py
│   ├── rental.py
│   └── invoice.py
│
├── payments/
│   ├── __init__.py
│   ├── payment_processor.py
│   ├── card_payment.py
│   └── upi_payment.py
│
├── exceptions/
│   ├── __init__.py
│   └── rental_exceptions.py
│
└── services/
    ├── __init__.py
    └── rental_service.py
```

---

## 4. Class Responsibilities

### 4.1 Vehicle

`Vehicle` is the abstract base class for all vehicle types.

It contains common vehicle information:

- Vehicle ID
- Registration number
- Brand
- Model
- Daily rental rate
- Availability status

It provides common operations such as:

- `calculate_rental_cost()`
- `display_details()`
- `mark_as_rented()`
- `mark_as_available()`

The Vehicle class defines common behaviour while allowing subclasses to
provide their own rental-cost calculation.

---

### 4.2 Car

`Car` inherits from `Vehicle`.

The rental cost for a car is:

```text
Daily rate × Rental days
```

Example:

```text
₹2,000 × 3 days = ₹6,000
```

---

### 4.3 Bike

`Bike` inherits from `Vehicle`.

The normal rental cost is calculated using the daily rate and rental days.

When the rental period exceeds five days, a 5% discount is applied.

---

### 4.4 Van

`Van` inherits from `Vehicle`.

The van rental cost consists of:

```text
Daily rate × Rental days + Service charge
```

---

### 4.5 Customer

`Customer` stores customer information:

- Customer ID
- Name
- Email
- Driving licence number
- Rental history

The class provides methods to:

- Add a rental
- Display previous rentals

Customer fields are kept private and accessed through controlled methods or
properties.

---

### 4.6 Rental

`Rental` represents a vehicle rental transaction.

It contains information such as:

- Rental ID
- Customer
- Vehicle
- Rental date
- Return date
- Number of rental days
- Total amount
- Rental status
- Payment processor
- Invoice

It provides methods to:

- Calculate the final rental amount
- Complete a rental
- Record the return date

---

### 4.7 Invoice

`Invoice` represents the final bill for a rental.

It contains:

- Rental information
- Base rental amount
- Late fee
- Final amount

It provides methods to:

- Generate the invoice
- Display the invoice

---

### 4.8 PaymentProcessor

`PaymentProcessor` is the payment abstraction / contract.

It defines the common payment operation:

```python
process_payment(amount)
```

The rental service depends on this abstraction instead of depending directly
on one particular payment method.

---

### 4.9 CardPayment

`CardPayment` provides card-based payment processing.

It implements the payment operation defined by the payment abstraction.

---

### 4.10 UPIPayment

`UPIPayment` provides UPI-based payment processing.

It implements the same payment operation as the other payment methods.

---

### 4.11 RentalService

`RentalService` coordinates the main rental workflow.

Its responsibilities include:

1. Validate rental days.
2. Check vehicle availability.
3. Calculate rental cost.
4. Process payment.
5. Confirm the rental only after successful payment.
6. Mark the vehicle as rented.
7. Create the rental record.
8. Create the invoice.
9. Add the rental to customer history.
10. Return vehicles.
11. Search available vehicles by type.

---

## 5. OOP Concepts Demonstrated

### 5.1 Encapsulation

Encapsulation is used to protect the internal state of objects.

Important fields are kept private using double-underscore attributes.

Examples:

```python
self.__vehicle_id
self.__name
self.__rental_history
self.__total_amount
```

Controlled access is provided through methods and properties.

This prevents other parts of the application from directly modifying the
internal state of objects.

---

### 5.2 Abstraction

Abstraction is used through the abstract `Vehicle` class and the
`PaymentProcessor` contract.

`Vehicle` defines common behaviour for all vehicles while allowing each
subclass to provide its own implementation.

Similarly, `PaymentProcessor` defines the common payment operation without
forcing the rental service to know how a particular payment method works.

---

### 5.3 Inheritance

Inheritance is used to create specialized vehicle classes.

```text
Vehicle
   │
   ├── Car
   ├── Bike
   └── Van
```

`Car`, `Bike`, and `Van` inherit common properties and behaviour from
`Vehicle`.

This avoids duplicating common vehicle code.

---

### 5.4 Polymorphism

Polymorphism is one of the most important concepts demonstrated in this
project.

Each vehicle type provides its own implementation of:

```python
calculate_rental_cost(days)
```

For example:

```python
vehicle.calculate_rental_cost(days)
```

The caller does not need to determine whether the object is a Car, Bike, or
Van.

The appropriate implementation is selected automatically based on the
actual object.

Therefore, the rental service does not need a large conditional structure
such as:

```python
if vehicle_type == "Car":
    ...
elif vehicle_type == "Bike":
    ...
elif vehicle_type == "Van":
    ...
```

This makes the design cleaner and easier to extend.

For example, if a new vehicle type such as `SUV` is added, it can inherit from
`Vehicle` and provide its own `calculate_rental_cost()` implementation
without changing the existing vehicle calculation logic.

---

### 5.5 Method Overriding

`Car`, `Bike`, and `Van` override the rental-cost calculation defined by
`Vehicle`.

This allows each vehicle type to implement its own business rule.

---

### 5.6 Composition

The system uses composition/strong object relationships between objects.

A `Rental` contains references to:

- Customer
- Vehicle
- Payment processor
- Invoice

This allows the rental object to represent the complete rental transaction.

---

### 5.7 Association

A customer can have multiple rental records over time.

Conceptually:

```text
Customer
   │
   ├── Rental 1
   ├── Rental 2
   └── Rental 3
```

The customer's rental history stores these rental records.

---

### 5.8 Dependency Inversion

`RentalService` depends on the `PaymentProcessor` abstraction rather than
directly depending on `CardPayment` or `UPIPayment`.

Therefore, the same rental workflow can work with different payment methods.

For example:

```python
rental_service.create_rental(
    ...,
    card_payment
)
```

or:

```python
rental_service.create_rental(
    ...,
    upi_payment
)
```

The rental service itself does not need to be changed.

---

### 5.9 Exception Handling

Custom exceptions are used to handle invalid operations.

Examples include:

```text
RentalError
    │
    ├── InvalidRentalDaysError
    ├── VehicleUnavailableError
    └── PaymentFailedError
```

These provide meaningful error messages instead of allowing invalid
operations to continue.

---

## 6. Business Rules

The system follows these business rules:

1. Rental days must be greater than zero.
2. A customer cannot rent an unavailable vehicle.
3. The same vehicle cannot be rented by two customers at the same time.
4. Vehicles must have valid registration information.
5. Payment must succeed before the rental is confirmed.
6. Sensitive payment information is not stored as plain text.
7. A returned vehicle becomes available again.
8. Invalid operations produce meaningful error messages.

---

## 7. Rental Cost Rules

### Car

```text
Car cost = Daily rate × Rental days
```

For example:

```text
₹2,000 × 3 = ₹6,000
```

---

### Bike

A 5% discount is applied when the rental exceeds five days.

```text
Normal cost = Daily rate × Rental days

Discount = 5% of normal cost

Final cost = Normal cost - Discount
```

---

### Van

```text
Van cost = Daily rate × Rental days + Service charge
```

For example:

```text
₹3,000 × 2 + ₹500
= ₹6,500
```

---

## 8. Late-Fee Rule

The late fee is calculated using:

```text
Late fee =
Number of late days × 20% × Vehicle daily rental rate
```

For the mandatory scenario:

```text
Daily rate = ₹2,000
Late days = 1

Late fee
= 1 × 20% × ₹2,000
= ₹400
```

Therefore:

```text
Base amount = ₹6,000
Late fee    = ₹400
Final amount = ₹6,400
```

---

## 9. Rental Workflow

The complete rental workflow is:

```text
Customer
    │
    ▼
Select vehicle
    │
    ▼
Enter rental days
    │
    ▼
Validate rental days
    │
    ▼
Check vehicle availability
    │
    ▼
Calculate rental cost
    │
    ▼
Process payment
    │
    ├── Payment fails
    │       │
    │       ▼
    │   Rental rejected
    │
    └── Payment succeeds
            │
            ▼
      Mark vehicle rented
            │
            ▼
       Create Rental
            │
            ▼
       Create Invoice
            │
            ▼
     Update customer history
```

---

## 10. Vehicle Return Workflow

When a vehicle is returned:

```text
Rental
   │
   ▼
Record return date
   │
   ▼
Determine late days
   │
   ▼
Calculate late fee
   │
   ▼
Calculate final amount
   │
   ▼
Complete rental
   │
   ▼
Mark vehicle available
```

---

## 11. Mandatory Demonstration Scenario

The assignment requires the following demonstration:

1. Add one car, one bike, and one van.
2. Register two customers.
3. Display all available vehicles.
4. Customer A rents the car for three days.
5. Attempt to rent the same car to Customer B.
6. Display an appropriate vehicle-unavailable message.
7. Process Customer A's payment successfully.
8. Return the car one day late.
9. Calculate the base amount, late fee, and final amount.
10. Display the final invoice.
11. Confirm that the returned car is available again.
12. Display Customer A's rental history.

The implemented system successfully demonstrates this workflow.

Expected calculation:

```text
Vehicle: V101
Vehicle type: Car
Daily rate: ₹2,000
Rental duration: 3 days

Base rental amount:
₹2,000 × 3 = ₹6,000

Late days:
1

Late fee:
1 × 20% × ₹2,000 = ₹400

Final amount:
₹6,000 + ₹400 = ₹6,400
```

---

## 12. Vehicle Search

The system supports searching available vehicles by vehicle type.

Example:

```python
rental_service.search_vehicles_by_type(
    vehicles,
    "Car"
)
```

Only available vehicles matching the requested type are returned.

---

## 13. Exception Scenarios Tested

The following failure scenarios have been tested successfully.

### Invalid rental days

```text
Input: 0 days

Result:
InvalidRentalDaysError
```

---

### Unavailable vehicle

```text
Input:
Vehicle is already rented

Result:
VehicleUnavailableError
```

---

### Payment failure

```text
Payment processing returns False

Result:
PaymentFailedError
```

The rental is not confirmed when payment fails.

---

## 14. Testing Results

The following scenarios were tested successfully:

| Test Case | Expected Result | Status |
|---|---|---|
| Successful car rental | Rental created | PASS |
| Invalid rental days | Exception raised | PASS |
| Unavailable vehicle | Exception raised | PASS |
| Payment failure | Rental rejected | PASS |
| Bike rental | Bike rental rule applied | PASS |
| Van rental | Service charge applied | PASS |
| One-day late return | ₹400 late fee | PASS |
| Vehicle return | Vehicle becomes available | PASS |
| Customer rental history | Rental recorded | PASS |
| Search by vehicle type | Matching available vehicles returned | PASS |

---

## 15. Class Diagram

The class diagram is stored in:

```text
class_diagram.png
```

It shows:

- Vehicle inheritance hierarchy
- Car, Bike, and Van relationships
- PaymentProcessor abstraction
- CardPayment and UPIPayment
- Customer and Rental association
- Rental and Vehicle relationship
- Rental and Invoice relationship
- RentalService dependencies
- Major OOP concepts used in the project

![Vehicle Rental System Class Diagram](class_diagram.png)

---

## 16. How to Run the Project

### Prerequisites

Python 3.x must be installed.

Check the installed Python version:

```bash
python --version
```

---

### Run the application

Open a terminal in the project root directory:

```bash
cd vehicle_rental_system
```

Run:

```bash
python main.py
```

The program will execute the vehicle rental demonstration and display the
results in the console.

---

## 17. Example Console Output

A successful mandatory demonstration should include output similar to:

```text
AVAILABLE VEHICLES

V101 | Car | Toyota | Innova | Rs. 2000.00/day | Available
V102 | Bike | Yamaha | FZ | Rs. 700.00/day | Available
V103 | Van | Tata | Winger | Rs. 3000.00/day | Available

CUSTOMER A RENTAL

Payment completed successfully.
Rental created successfully.

CUSTOMER B ATTEMPT

Vehicle unavailable: Vehicle V101 is unavailable.

VEHICLE RETURN

Vehicle returned successfully.
Late days: 1

FINAL INVOICE

Base rental amount: Rs. 6000.00
Late fee: Rs. 400.00
Final amount: Rs. 6400.00

VEHICLE STATUS AFTER RETURN

V101 ... Available
```

Actual formatting may vary slightly depending on the console output.

---

## 18. Technologies Used

- Python 3
- Object-Oriented Programming
- Abstract Base Classes
- Python packages and modules
- Exception handling

---

## 19. Design Benefits

The application is divided into separate packages and classes instead of
placing the entire application into one class.

This provides:

- Clear separation of responsibilities
- Code reuse
- Easier maintenance
- Easier testing
- Extensibility
- Better application structure

The polymorphic vehicle design also allows new vehicle types to be added
without modifying the existing rental-cost calculation logic.

---

## 20. Conclusion

The Vehicle Rental Management System demonstrates how Object-Oriented
Programming can be used to model a real-world business problem.

The application implements vehicle management, customer management,
rental processing, payment abstraction, invoice generation, vehicle return,
late-fee calculation, exception handling, and customer rental history.

The project also demonstrates encapsulation, abstraction, inheritance,
polymorphism, method overriding, composition, association, dependency
inversion, and exception handling.