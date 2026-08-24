from .payment_processor import PaymentProcessor


class UPIPayment(PaymentProcessor):

    def __init__(self, upi_id):
        self.__upi_id = upi_id

    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        print(f"Processing UPI payment for {self.__upi_id}...")
        print(f"UPI payment of Rs. {amount:.2f} completed successfully.")

        return True