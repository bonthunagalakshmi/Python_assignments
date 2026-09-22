class RentalError(Exception):
    """Base exception for expected DriveEase business errors."""


class ValidationError(RentalError):
    """Raised when user-provided data is invalid."""


class CustomerNotFoundError(RentalError):
    """Raised when a customer ID cannot be found."""


class VehicleNotFoundError(RentalError):
    """Raised when a vehicle ID cannot be found."""


class VehicleUnavailableError(RentalError):
    """Raised when a vehicle cannot be booked for the requested period."""


class InvalidRentalPeriodError(RentalError):
    """Raised when the pickup/return period is invalid."""


class RentalNotFoundError(RentalError):
    """Raised when a rental ID cannot be found."""


class PaymentError(RentalError):
    """Raised when simulated payment validation fails."""


class MaintenanceError(RentalError):
    """Raised when a maintenance operation is not allowed."""