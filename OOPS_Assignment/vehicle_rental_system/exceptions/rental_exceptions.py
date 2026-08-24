class RentalError(Exception):
    """Base exception for rental-related errors."""
    pass


class InvalidRentalDaysError(RentalError):
    """Raised when rental days are invalid."""
    pass


class VehicleUnavailableError(RentalError):
    """Raised when a vehicle is already rented."""
    pass


class PaymentFailedError(RentalError):
    """Raised when payment processing fails."""
    pass