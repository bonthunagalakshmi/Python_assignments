from .base import BaseView, tk, ttk


class CustomerView(BaseView):
    def build(self, parent):
        super().build(parent)
        header = ttk.Frame(self.frame)
        header.pack(fill="x")
        self.title("Customers", "Register and search the people who rent from your office.")
        controls = ttk.Frame(self.frame)
        controls.pack(fill="x")
        self.search_value = tk.StringVar()
        ttk.Entry(controls, textvariable=self.search_value, width=32).pack(side="left")
        ttk.Button(controls, text="Search", command=self.refresh).pack(side="left", padx=8)
        ttk.Button(controls, text="Add customer", style="Accent.TButton", command=self.add_customer).pack(side="right")
        self.customer_tree = self.tree([
            ("customer_id", "ID", 90), ("name", "Name", 160), ("email", "Email", 190),
            ("phone", "Phone", 130), ("driving_licence", "Licence", 130),
            ("registration_date", "Registered", 110), ("status", "Status", 90),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "customer_tree"):
            return
        self.clear_tree(self.customer_tree)
        for row in self.app.customers.search_customers(self.search_value.get()):
            self.customer_tree.insert("", "end", values=(
                row["customer_id"], row["name"], row["email"], row["phone"],
                row["driving_licence"], row["registration_date"], row["status"],
            ))

    def add_customer(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add customer")
        dialog.transient(self.app.root)
        dialog.grab_set()
        fields = [("Name", "name"), ("Email", "email"), ("Phone", "phone"),
                  ("Driving licence", "licence"), ("Address", "address")]
        entries = {}
        for row, (label, key) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=16, pady=8, sticky="w")
            entry = ttk.Entry(dialog, width=38)
            entry.grid(row=row, column=1, padx=16, pady=8)
            entries[key] = entry
        def save():
            try:
                self.app.customers.create_customer(
                    entries["name"].get(), entries["email"].get(), entries["phone"].get(),
                    entries["licence"].get(), entries["address"].get(),
                )
                dialog.destroy()
                self.refresh()
                self.app.refresh_all()
            except Exception as error:
                self.error(error)
        ttk.Button(dialog, text="Save customer", style="Accent.TButton", command=save).grid(
            row=len(fields), column=0, columnspan=2, pady=16
        )