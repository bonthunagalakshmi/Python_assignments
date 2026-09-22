from .base import BaseView, tk, ttk


class ReturnView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Return vehicle", "Record the inspection and close a confirmed or active rental.")
        form = ttk.Frame(self.frame)
        form.pack(fill="x")
        self.rental_value = tk.StringVar()
        self.actual_date = tk.StringVar()
        self.odometer = tk.StringVar()
        self.fuel = tk.StringVar()
        self.condition = tk.StringVar(value="GOOD")
        self.remarks = tk.StringVar()
        fields = [
            ("Rental ID", self.rental_value), ("Actual return (YYYY-MM-DD)", self.actual_date),
            ("Return odometer", self.odometer), ("Return fuel %", self.fuel),
            ("Condition", self.condition), ("Damage / remarks", self.remarks),
        ]
        for index, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=index // 3 * 2, column=index % 3, sticky="w", padx=(0, 10), pady=(0, 3))
            ttk.Entry(form, textvariable=variable, width=23).grid(row=index // 3 * 2 + 1, column=index % 3, sticky="w", padx=(0, 16), pady=(0, 10))
        ttk.Button(self.frame, text="Calculate charges and complete return", style="Accent.TButton", command=self.submit).pack(anchor="w", pady=10)
        self.rental_tree = self.tree([
            ("rental_id", "Rental", 95), ("vehicle_id", "Vehicle", 95),
            ("customer_id", "Customer", 95), ("pickup_date", "Pickup", 105),
            ("return_date", "Due", 105), ("final_amount", "Current total", 110),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "rental_tree"):
            return
        self.clear_tree(self.rental_tree)
        for row in self.app.rentals.list_rentals():
            if row["status"] in {"CONFIRMED", "ACTIVE"}:
                self.rental_tree.insert("", "end", values=(
                    row["rental_id"], row["vehicle_id"], row["customer_id"],
                    row["pickup_date"], row["return_date"], f"₹{float(row['final_amount']):,.2f}",
                ))

    def submit(self):
        try:
            rental, invoice, charges = self.app.rentals.return_vehicle(
                self.rental_value.get(), self.actual_date.get(), self.odometer.get(),
                self.fuel.get(), self.condition.get(), self.remarks.get(),
            )
            self.info(
                f"Return completed for {rental['rental_id']}.\n"
                f"Additional charges: ₹{charges['total']:,.2f}\n"
                f"Outstanding balance: ₹{float(invoice['amount_due']):,.2f}"
            )
            self.refresh()
            self.app.refresh_all()
        except Exception as error:
            self.error(error)