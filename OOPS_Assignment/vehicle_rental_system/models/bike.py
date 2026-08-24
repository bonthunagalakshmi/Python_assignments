from .vehicle import Vehicle


class Bike(Vehicle):

    def calculate_rental_cost(self, days):
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        amount = self.daily_rate * days

        if days > 5:
            amount = amount * 0.95

        return amount