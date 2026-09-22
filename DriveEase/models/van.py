from .vehicle import Vehicle


class Van(Vehicle):
    def calculate_rental_cost(self, days: int) -> float:
        # Vans include a transparent ₹150/day handling allowance.
        return round((self.daily_rate + 150) * days, 2)