from .vehicle import Vehicle


class Bike(Vehicle):
    def calculate_rental_cost(self, days: int) -> float:
        # A modest 10% multi-day discount reflects lower operating cost.
        discount = 0.90 if days >= 3 else 1.0
        return round(self.daily_rate * days * discount, 2)