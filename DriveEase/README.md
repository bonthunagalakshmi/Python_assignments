# DriveEase — Vehicle Rental & Fleet Management

DriveEase is a staff-side desktop application for a small vehicle-rental office. It demonstrates a complete internship-level workflow: register a customer, manage the fleet, search availability by dates, quote and confirm a rental, simulate a payment, inspect a returned vehicle, collect additional charges, and review live reports.

This is a local desktop application, not a commercial production system. It intentionally does not include online booking, authentication, real payment gateways, cloud storage, SMS/email, multi-user concurrency, or government licence verification.

## Features

- Customer registration with automatic `CUS1001`-style IDs and validation
- Car, Bike, and Van fleet management with unique registration numbers
- Vehicle status tracking: `AVAILABLE`, `RESERVED`, `RENTED`, `MAINTENANCE`
- Date-based availability and overlap protection
- Quotations with vehicle-specific pricing, discounts, 18% tax, and transparent totals
- Simulated UPI, Card, and Cash payments; no raw card or PIN data is stored
- Multiple payments for a rental and invoice states `UNPAID`, `PARTIAL`, and `PAID`
- Return inspections for odometer, fuel, condition, and damage remarks
- Late, fuel-shortage, and damage charges
- Maintenance records and return-to-service workflow
- Dashboard, rental history, revenue, utilization, payment-method, and customer-spending reports
- Excel persistence through `DriveEase_Data.xlsx`
- Sample data on first launch only; startup never duplicates it

## Technology

- Python 3
- Tkinter / ttk for the GUI
- `openpyxl` for Excel persistence
- Python standard library for the application services and tests

## Folder structure

```text
DriveEase/
├── main.py
├── README.md
├── requirements.txt
├── test_system.py
├── models/          # Vehicle hierarchy, Customer, Rental, Invoice, Payment
├── services/        # Customer, fleet, pricing, rental, payment, maintenance, reports
├── payments/        # Abstract payment processor and UPI/Card/Cash implementations
├── data/            # Excel workbook gateway and first-launch sample data
├── ui/              # Tkinter shell and staff pages
├── exceptions/      # Expected business errors
└── utils/           # ID generation and validation helpers
```

`DriveEase_Data.xlsx` is created next to `main.py` when the application starts. It is not committed as source code and is safe to delete when a fresh local demo is needed.

## Installation and run

From the project directory:

```bash
python -m pip install -r requirements.txt
python main.py
```

The GUI requires a Python build with Tk support. The business services, persistence, and test suite can still be run on a headless machine.

## Main workflow

1. Register a customer.
2. Add or review fleet vehicles.
3. Enter pickup and return dates on **New Rental**.
4. Search available vehicles for the whole period.
5. Select a vehicle and process a simulated payment.
6. DriveEase writes the rental, payment, and invoice to Excel.
7. Use **Return Vehicle** to enter the return inspection.
8. Late, fuel, and damage charges update the final invoice.
9. Collect the remaining balance through another simulated payment.
10. Use **Maintenance** and **Reports** for the remaining office workflow.

## Excel persistence

The workbook contains `Customers`, `Vehicles`, `Rentals`, `Payments`, `Invoices`, and `Maintenance` sheets. Each service reads current rows from the workbook and writes only the affected records. A new workbook gets headers and a small sample fleet/customer set exactly once; an existing workbook is opened without resetting its data.

## Date-overlap rule

Rental dates use a start-inclusive/end-exclusive convention. A requested period overlaps an existing confirmed/active booking when:

```text
existing_start < requested_end
AND
requested_start < existing_end
```

Therefore, `2026-09-20` to `2026-09-25` blocks `2026-09-22` to `2026-09-24`, but it does not block a new rental beginning on `2026-09-25`. Cancelled and completed rentals do not block future availability. A vehicle in maintenance is never rentable.

## Pricing rules

- Car: daily rate × rental days.
- Bike: daily rate × rental days, with a modest 10% multi-day discount for three or more days.
- Van: daily rate plus a transparent ₹150/day handling allowance.
- Final amount: `base rental + additional charges - discount + 18% tax`.
- Return charges: late days × daily rate × 1.25; fuel shortage × ₹30 per percentage point; ₹3,500 when the return is marked damaged/poor or contains damage remarks.

## Payment simulation

Payment classes share the abstract `PaymentProcessor` interface. UPI requires a VPA-like reference such as `staff@upi`; Card accepts only a masked value such as `****4242` or a token; Cash accepts an optional cash reference. Invalid payments raise an error before any confirmed rental, invoice, or payment record is written.

## OOP concepts demonstrated

- **Encapsulation:** `Vehicle` validates and controls status, rates, fuel, odometer, and other state.
- **Abstraction:** `Vehicle` and `PaymentProcessor` are abstract base classes.
- **Inheritance:** `Car`, `Bike`, and `Van` inherit from `Vehicle`; each payment class inherits from `PaymentProcessor`.
- **Polymorphism:** `calculate_rental_cost()` varies by vehicle type, and the payment service selects the correct processor implementation.
- **Composition/association:** `RentalService` coordinates customer, vehicle, pricing, payment, and invoice records.

## Testing

The tests use a temporary workbook and cover actual behavior rather than object existence:

```bash
python test_system.py
python -m compileall .
```

The suite covers workbook creation, unique IDs, search, availability, overlap rejection, boundary acceptance, pricing, polymorphism, all payment paths, failed-payment safety, invoices, partial/final payment, return charges, maintenance, reports, and restart persistence.

## How I would explain this project to a trainer

- **Why Tkinter?** It is included with Python and is sufficient for a small staff desktop tool without introducing a web stack.
- **Why Excel?** The brief calls for a local internship-scale system without a database server; `openpyxl` provides transparent, inspectable persistence.
- **Why services?** Pricing, availability, payments, returns, and reports stay testable and independent from button handlers.
- **Where is encapsulation?** `Vehicle` validates fields and exposes controlled status changes.
- **Where is abstraction?** `Vehicle` and `PaymentProcessor` define contracts for their subclasses.
- **Where is inheritance?** Car/Bike/Van and UPI/Card/Cash share their respective base classes.
- **Where is polymorphism?** Rental cost and payment validation depend on the concrete subtype selected at runtime.
- **How does availability work?** It checks date overlap against confirmed/active rentals, not a single boolean.
- **How does payment work?** It is a safe simulation that stores method, amount, date, status, and a masked/reference value only.
- **How does return inspection work?** The return records odometer, fuel, condition, remarks, and transparent additional charges.
- **How are reports generated?** `ReportService` reads current Excel rows and calculates summaries each time, so reports change with the data.

## Known limitations

Tkinter widgets need a display server. On a headless environment, the domain layer and tests run normally, but launching the GUI reports that Tk support/display is unavailable instead of claiming a GUI interaction test was performed.