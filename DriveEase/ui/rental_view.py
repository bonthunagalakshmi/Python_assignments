from .base import BaseView, tk, ttk


class RentalView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("New rental", "Search by dates first, then create a quotation and simulated payment.")
        form = ttk.Frame(self.frame)
        form.pack(fill="x")
        self.customer_value = tk.StringVar()
        self.pickup_value = tk.StringVar()
        self.return_value = tk.StringVar()
        self.vehicle_value = tk.StringVar()
        for column, label, variable in [
            (0, "Customer ID", self.customer_value), (1, "Pickup (YYYY-MM-DD)", self.pickup_value),
            (2, "Return (YYYY-MM-DD)", self.return_value),
        ]:
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=(0, 8))
            ttk.Entry(form, textvariable=variable, width=20).grid(row=1, column=column, padx=(0, 12), pady=(4, 12))
        ttk.Button(form, text="Find available vehicles", style="Accent.TButton", command=self.find).grid(row=1, column=3)
        self.available_tree = self.tree([
            ("vehicle_id", "ID", 100), ("registration_number", "Registration", 120),
            ("vehicle_type", "Type", 80), ("brand", "Brand", 120), ("model", "Model", 120),
            ("daily_rate", "Daily rate", 100),
        ])
        action = ttk.Frame(self.frame)
        action.pack(fill="x", pady=14)
        ttk.Label(action, text="Payment method").pack(side="left")
        self.method_value = tk.StringVar(value="CASH")
        ttk.Combobox(action, textvariable=self.method_value, values=["CASH", "UPI", "CARD"], state="readonly", width=10).pack(side="left", padx=8)
        ttk.Label(action, text="Reference (UPI or ****1234)").pack(side="left")
        self.reference_value = tk.StringVar()
        ttk.Entry(action, textvariable=self.reference_value, width=20).pack(side="left", padx=8)
        ttk.Button(action, text="Confirm selected rental", command=self.confirm).pack(side="right")
        return self.frame

    def find(self):
        try:
            rows = self.app.rentals.available_vehicles(self.pickup_value.get(), self.return_value.get())
            self.clear_tree(self.available_tree)
            for row in rows:
                self.available_tree.insert("", "end", values=(
                    row["vehicle_id"], row["registration_number"], row["vehicle_type"],
                    row["brand"], row["model"], f"₹{float(row['daily_rate']):,.0f}",
                ))
        except Exception as error:
            self.error(error)

    def confirm(self):
        selected = self.available_tree.selection()
        if not selected:
            self.error(ValueError("Select a vehicle from the available list first."))
            return
        vehicle_id = self.available_tree.item(selected[0], "values")[0]
        try:
            rental, invoice, payment = self.app.rentals.confirm_rental(
                self.customer_value.get(), vehicle_id, self.pickup_value.get(), self.return_value.get(),
                self.method_value.get(), self.reference_value.get(),
            )
            self.info(f"Rental {rental.rental_id} confirmed.\nInvoice {invoice['invoice_id']} • {payment.amount:,.2f} paid.")
            self.app.refresh_all()
            self.find()
        except Exception as error:
            self.error(error)