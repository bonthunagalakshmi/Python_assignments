class Customer:

    def __init__(
        self,
        customer_id,
        name,
        email,
        licence_number
    ):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__licence_number = licence_number
        self.__rental_history = []

        self.__validate_customer()

    def __validate_customer(self):
        if not self.__customer_id:
            raise ValueError("Customer ID cannot be empty.")

        if not self.__name:
            raise ValueError("Customer name cannot be empty.")

        if not self.__email:
            raise ValueError("Email address cannot be empty.")

        if not self.__licence_number:
            raise ValueError("Driving licence number cannot be empty.")

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def licence_number(self):
        return self.__licence_number

    def add_rental(self, rental):
        self.__rental_history.append(rental)

    def display_rental_history(self):
        print(f"\nRental History - {self.__name}")
        print("-" * 50)

        if not self.__rental_history:
            print("No rental history found.")
            return

        for rental in self.__rental_history:
            print(rental)