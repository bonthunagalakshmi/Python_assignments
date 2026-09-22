from .vehicle import Vehicle


class Car(Vehicle):
    def calculate_rental_cost(self, days: int) -> float:
        return round(self.daily_rate * days, 2)