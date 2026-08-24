from .vehicle import Vehicle


class Van(Vehicle):

    def __init__(
        self,
        vehicle_id,
        registration_number,
        brand,
        model,
        daily_rate,
        service_charge
    ):
        super().__init__(
            vehicle_id,
            registration_number,
            brand,
            model,
            daily_rate
        )

        if service_charge < 0:
            raise ValueError("Service charge cannot be negative.")

        self.__service_charge = service_charge

    @property
    def service_charge(self):
        return self.__service_charge

    def calculate_rental_cost(self, days):
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        return (self.daily_rate * days) + self.__service_charge