from .base import BaseView, tk, ttk


class MaintenanceView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Maintenance", "Take vehicles out of service and return them to the available fleet when complete.")
        form = ttk.Frame(self.frame)
        form.pack(fill="x")
        self.vehicle_id = tk.StringVar()
        self.reason = tk.StringVar()
        self.cost = tk.StringVar(value="0")
        self.notes = tk.StringVar()
        for column, label, variable in [
            (0, "Vehicle ID", self.vehicle_id), (1, "Reason", self.reason),
            (2, "Cost", self.cost), (3, "Notes", self.notes),
        ]:
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=(0, 8))
            ttk.Entry(form, textvariable=variable, width=22).grid(row=1, column=column, padx=(0, 12), pady=(4, 10))
        ttk.Button(form, text="Start maintenance", style="Accent.TButton", command=self.start).grid(row=1, column=4)
        self.tree_widget = self.tree([
            ("maintenance_id", "Record", 100), ("vehicle_id", "Vehicle", 100),
            ("date", "Date", 110), ("reason", "Reason", 180), ("cost", "Cost", 90),
            ("notes", "Notes", 180), ("status", "Status", 100),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "tree_widget"):
            return
        self.clear_tree(self.tree_widget)
        for row in self.app.maintenance.list_records():
            self.tree_widget.insert("", "end", values=(
                row["maintenance_id"], row["vehicle_id"], row["date"], row["reason"],
                f"₹{float(row['cost']):,.2f}", row["notes"], row["status"],
            ))

    def start(self):
        try:
            self.app.maintenance.start_maintenance(
                self.vehicle_id.get(), self.reason.get(), self.cost.get(), self.notes.get()
            )
            self.refresh()
            self.app.refresh_all()
        except Exception as error:
            self.error(error)