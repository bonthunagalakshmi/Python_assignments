from .base import BaseView, ttk


class InvoiceView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Invoices", "Review totals, paid amounts, and balances due.")
        self.invoice_tree = self.tree([
            ("invoice_id", "Invoice", 95), ("rental_id", "Rental", 95),
            ("customer_id", "Customer", 95), ("vehicle_id", "Vehicle", 95),
            ("total", "Total", 100), ("amount_paid", "Paid", 100),
            ("amount_due", "Due", 100), ("payment_status", "Payment status", 110),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "invoice_tree"):
            return
        self.clear_tree(self.invoice_tree)
        for row in self.app.excel.read_records("Invoices"):
            self.invoice_tree.insert("", "end", values=(
                row["invoice_id"], row["rental_id"], row["customer_id"], row["vehicle_id"],
                f"₹{float(row['total']):,.2f}", f"₹{float(row['amount_paid']):,.2f}",
                f"₹{float(row['amount_due']):,.2f}", row["payment_status"],
            ))