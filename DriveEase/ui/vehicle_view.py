from .base import BaseView, tk, ttk


class VehicleView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Fleet", "Search the fleet, inspect live status, and add vehicles.")
        controls = ttk.Frame(self.frame)
        controls.pack(fill="x")
        self.search_value = tk.StringVar()
        self.type_value = tk.StringVar(value="ALL")
        self.status_value = tk.StringVar(value="ALL")
        ttk.Entry(controls, textvariable=self.search_value, width=25).pack(side="left")
        ttk.Combobox(controls, textvariable=self.type_value, values=["ALL", "CAR", "BIKE", "VAN"], width=10, state="readonly").pack(side="left", padx=6)
        ttk.Combobox(controls, textvariable=self.status_value, values=["ALL", "AVAILABLE", "RESERVED", "RENTED", "MAINTENANCE"], width=14, state="readonly").pack(side="left")
        ttk.Button(controls, text="Filter", command=self.refresh).pack(side="left", padx=8)
        ttk.Button(controls, text="Add vehicle", style="Accent.TButton", command=self.add_vehicle).pack(side="right")
        self.vehicle_tree = self.tree([
            ("vehicle_id", "ID", 90), ("registration_number", "Registration", 110),
            ("vehicle_type", "Type", 75), ("brand", "Brand", 110), ("model", "Model", 110),
            ("daily_rate", "Daily rate", 90), ("fuel_level", "Fuel %", 65),
            ("condition", "Condition", 90), ("status", "Status", 110),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "vehicle_tree"):
            return
        self.clear_tree(self.vehicle_tree)
        for row in self.app.fleet.search(self.search_value.get(), self.type_value.get(), self.status_value.get()):
            self.vehicle_tree.insert("", "end", values=(
                row["vehicle_id"], row["registration_number"], row["vehicle_type"],
                row["brand"], row["model"], f"₹{float(row['daily_rate']):,.0f}",
                row["fuel_level"], row["condition"], row["status"],
            ))

    def add_vehicle(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add vehicle")
        dialog.transient(self.app.root)
        dialog.grab_set()
        fields = [
            ("Type (Car/Bike/Van)", "type", "Car"), ("Registration", "registration", ""),
            ("Brand", "brand", ""), ("Model", "model", ""), ("Year", "year", "2024"),
            ("Fuel type", "fuel", "Petrol"), ("Transmission", "transmission", "Manual"),
            ("Seats", "seats", "5"), ("Daily rate", "rate", "2000"),
            ("Odometer", "odometer", "0"), ("Fuel level", "fuel_level", "100"),
        ]
        entries = {}
        for row, (label, key, default) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=14, pady=5, sticky="w")
            entry = ttk.Entry(dialog, width=30)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=14, pady=5)
            entries[key] = entry
        def save():
            try:
                self.app.fleet.add_vehicle(
                    entries["type"].get(), entries["registration"].get(), entries["brand"].get(),
                    entries["model"].get(), entries["year"].get(), entries["fuel"].get(),
                    entries["transmission"].get(), entries["seats"].get(), entries["rate"].get(),
                    entries["odometer"].get(), entries["fuel_level"].get(),
                )
                dialog.destroy()
                self.refresh()
                self.app.refresh_all()
            except Exception as error:
                self.error(error)
        ttk.Button(dialog, text="Save vehicle", style="Accent.TButton", command=save).grid(
            row=len(fields), column=0, columnspan=2, pady=14
        )