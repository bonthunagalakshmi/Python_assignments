from .vehicle import Vehicle


class Car(Vehicle):

    def calculate_rental_cost(self, days):
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        return self.daily_rate * days