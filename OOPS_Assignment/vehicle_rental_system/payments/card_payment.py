from .payment_processor import PaymentProcessor


class CardPayment(PaymentProcessor):

    def __init__(self, card_holder):
        self.__card_holder = card_holder

    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        print(f"Processing card payment for {self.__card_holder}...")
        print(f"Card payment of Rs. {amount:.2f} completed successfully.")

        return True