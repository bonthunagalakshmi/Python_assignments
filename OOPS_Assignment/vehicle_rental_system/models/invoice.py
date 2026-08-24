class Invoice:

    def __init__(self, rental):
        self.__rental = rental
        self.__base_amount = 0
        self.__late_fee = 0
        self.__final_amount = 0

    @property
    def rental(self):
        return self.__rental

    @property
    def base_amount(self):
        return self.__base_amount

    @property
    def late_fee(self):
        return self.__late_fee

    @property
    def final_amount(self):
        return self.__final_amount

    def generate(self, late_days=0):
        self.__base_amount = self.__rental.calculate_final_amount()

        if late_days < 0:
            raise ValueError("Late days cannot be negative.")

        self.__late_fee = (
            late_days
            * 0.20
            * self.__rental.vehicle.daily_rate
        )

        self.__final_amount = (
            self.__base_amount + self.__late_fee
        )

        return self.__final_amount

    def display(self):
        print("\nFINAL INVOICE")
        print("-" * 50)

        print("Rental ID:", self.__rental.rental_id)
        print("Customer:", self.__rental.customer.name)
        print("Vehicle:", self.__rental.vehicle.vehicle_id)
        print("Rental days:", self.__rental.days)

        print(f"Base rental amount: Rs. {self.__base_amount:.2f}")
        print(f"Late fee: Rs. {self.__late_fee:.2f}")
        print(f"Final amount: Rs. {self.__final_amount:.2f}")