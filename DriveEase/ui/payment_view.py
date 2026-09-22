from .base import BaseView, ttk


class PaymentView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Payments", "Every successful simulated payment is written to the Payments sheet.")
        self.payment_tree = self.tree([
            ("payment_id", "Payment", 95), ("rental_id", "Rental", 95), ("amount", "Amount", 100),
            ("payment_method", "Method", 95), ("payment_date", "Date", 110),
            ("status", "Status", 90), ("reference_id", "Reference", 150),
        ])
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "payment_tree"):
            return
        self.clear_tree(self.payment_tree)
        for row in self.app.payments.list_payments():
            self.payment_tree.insert("", "end", values=(
                row["payment_id"], row["rental_id"], f"₹{float(row['amount']):,.2f}",
                row["payment_method"], row["payment_date"], row["status"], row["reference_id"],
            ))